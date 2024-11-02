from typing import Callable, List, Generator
import os
import time
import json
import uuid

from dingo.exec.base import Executor
from dingo.data import dataset_map, datasource_map, Dataset
from dingo.model import Model
from dingo.model.modelres import ModelRes
from dingo.model.llm.base import BaseLLM
from dingo.model.rule.base import BaseRule
from dingo.io import InputArgs, MetaData, SummaryModel, ResultInfo
from dingo.utils import log


@Executor.register('local')
class LocalExecutor(Executor):

    def __init__(self, input_args: InputArgs):
        self.input_args = input_args
        self.summary: SummaryModel = SummaryModel()
        self.bad_info_list: List[ResultInfo] = []
        self.good_info_list: List[ResultInfo] = []
        self.summary_list: List[SummaryModel] = []

    def load_data(self) -> Generator[MetaData, None, None]:
        """
        Reads data from given path.

        **Run in executor.**

        Returns:
            Generator[MetaData]
        """
        new_input_args = self.input_args
        dataset_type = self.input_args.dataset
        source = self.input_args.datasource if self.input_args.datasource != "" else dataset_type
        dataset_cls = dataset_map[dataset_type]
        dataset: Dataset = dataset_cls(source=datasource_map[source](input_args=new_input_args))
        return dataset.get_data()

    def execute(self) -> List[SummaryModel]:
        input_path = self.input_args.input_path
        output_path = os.path.join(self.input_args.output_path, str(uuid.uuid1()))

        log.debug(str(self.input_args.eval_model))
        for model_name in [self.input_args.eval_model]:
            model, model_type = Model.get_model(model_name)

            model_path = output_path + '/' + model_name

            self.summary = SummaryModel(
                task_id=str(uuid.uuid1()),
                task_name=self.input_args.task_name,
                eval_model=model_name,
                input_path=input_path,
                output_path=output_path if self.input_args.save_data else '',
                create_time=time.strftime('%Y%m%d_%H%M%S', time.localtime()),
                score=0,
                num_good=0,
                num_bad=0,
                total=0,
                type_ratio={},
                name_ratio={}
            )
            self.evaluate(model, model_type)
            self.summarize()

            # pprint.pprint(record, sort_dicts=False)
            if self.input_args.save_data:
                if not os.path.exists(output_path):
                    os.makedirs(output_path)
                if not os.path.exists(model_path):
                    os.makedirs(model_path)
                self.write_data(model_path, model_type)

            self.summary_list.append(self.summary)

        log.debug(self.summary_list)
        return self.summary_list

    def evaluate(self, model, model_type):
        """
        get score (main progres).
        Args:
            model (Any): _description_
            model_type (str): _description_
        """
        log.debug('[get_score]:' + self.input_args.input_path)
        data_iter = self.load_data()

        for data in data_iter:
            if model_type == 'rule':
                self.evaluate_rule(model, data)
            elif model_type == 'llm':
                self.evaluate_llm(model, data)
            else:
                raise RuntimeError(f'Unsupported model type: {model_type}')
            self.summary.total += 1

        log.debug('[Summary]: ' + str(self.summary))

    def evaluate_rule(self, rule_map: List[BaseRule], d: MetaData):
        if_good = True
        result_info = ResultInfo(data_id=d.data_id, prompt=d.prompt, content=d.content)
        log.debug("[RuleMap]: " + str(rule_map))
        for r in rule_map:
            r_n = r.__name__
            # execute rule
            tmp: ModelRes = r.eval(d)
            # analyze result
            if tmp.error_status is False:
                continue
            if_good = False
            if tmp.type not in result_info.type_list:
                result_info.type_list.append(tmp.type)
            result_info.name_list.append(tmp.type + '-' + r_n)
            result_info.reason_list.append(tmp.reason)

        if if_good is True:
            if self.input_args.save_correct:
                result_info.type_list.append(ModelRes().type)
                result_info.name_list.append(ModelRes().type + '-' + ModelRes().name)
                self.good_info_list.append(result_info)
                t = ModelRes().type
                if t not in self.summary.type_ratio:
                    self.summary.type_ratio[t] = 1
                else:
                    self.summary.type_ratio[t] += 1
                n = ModelRes().type + '-' + ModelRes().name
                if n not in self.summary.name_ratio:
                    self.summary.name_ratio[n] = 1
                else:
                    self.summary.name_ratio[n] += 1
        else:
            self.bad_info_list.append(result_info)
            self.summary.num_bad += 1
            for t in result_info.type_list:
                if t not in self.summary.type_ratio:
                    self.summary.type_ratio[t] = 1
                else:
                    self.summary.type_ratio[t] += 1
            for n in result_info.name_list:
                if n not in self.summary.name_ratio:
                    self.summary.name_ratio[n] = 1
                else:
                    self.summary.name_ratio[n] += 1

    def evaluate_llm(self, llm: BaseLLM, d: MetaData):
        result_info = ResultInfo(data_id=d.data_id, prompt=d.prompt, content=d.content)
        tmp: ModelRes = llm.call_api(d)
        if tmp.error_status is True:
            if tmp.type not in result_info.type_list:
                result_info.type_list.append(tmp.type)
            result_info.name_list.append(tmp.type + '-' + tmp.name)
            result_info.reason_list.append(tmp.reason)
        else:
            if self.input_args.save_correct:
                if tmp.type not in result_info.type_list:
                    result_info.type_list.append(tmp.type)
                result_info.name_list.append(tmp.type + '-' + tmp.name)
                result_info.reason_list.append(tmp.reason)


        if tmp.error_status is False:
            if self.input_args.save_correct:
                self.good_info_list.append(result_info)
        else:
            self.bad_info_list.append(result_info)
            self.summary.num_bad += 1
        for t in result_info.type_list:
            if t not in self.summary.type_ratio:
                self.summary.type_ratio[t] = 1
            else:
                self.summary.type_ratio[t] += 1
        for n in result_info.name_list:
            if n not in self.summary.name_ratio:
                self.summary.name_ratio[n] = 1
            else:
                self.summary.name_ratio[n] += 1

    def summarize(self):
        if self.summary.total == 0:
            return
        self.summary.num_good = self.summary.total - self.summary.num_bad
        self.summary.score = round(self.summary.num_good / self.summary.total * 100, 2)
        for t in self.summary.type_ratio:
            self.summary.type_ratio[t] = round(self.summary.type_ratio[t] / self.summary.total, 6)
        for n in self.summary.name_ratio:
            self.summary.name_ratio[n] = round(self.summary.name_ratio[n] / self.summary.total, 6)
        self.summary.type_ratio = dict(sorted(self.summary.type_ratio.items()))
        self.summary.name_ratio = dict(sorted(self.summary.name_ratio.items()))

    def get_summary(self):
        return self.summary

    def get_bad_info_list(self):
        return self.bad_info_list

    def get_good_info_list(self):
        return self.good_info_list

    def write_data(self, path, model_type):
        for result_info in self.bad_info_list:
            for new_name in result_info.name_list:
                t = str(new_name).split('-')[0]
                n = str(new_name).split('-')[1]
                p_t = os.path.join(path, t)
                if not os.path.exists(p_t):
                    os.makedirs(p_t)
                f_n = os.path.join(path, t, n) + ".jsonl"
                with open(f_n, 'a', encoding='utf-8') as f:
                    str_json = json.dumps(result_info.to_dict(), ensure_ascii=False)
                    f.write(str_json + '\n')
        if self.input_args.save_correct:
            for result_info in self.good_info_list:
                for new_name in result_info.name_list:
                    t = str(new_name).split('-')[0]
                    n = str(new_name).split('-')[1]
                    p_t = os.path.join(path, t)
                    if not os.path.exists(p_t):
                        os.makedirs(p_t)
                    f_n = os.path.join(path, t, n) + ".jsonl"
                    with open(f_n, 'a', encoding='utf-8') as f:
                        str_json = json.dumps(result_info.to_dict(), ensure_ascii=False)
                        f.write(str_json + '\n')
        with open(path + '/summary.json', 'w', encoding='utf-8') as f:
            json.dump(self.summary.to_dict(), f, indent=4, ensure_ascii=False)
