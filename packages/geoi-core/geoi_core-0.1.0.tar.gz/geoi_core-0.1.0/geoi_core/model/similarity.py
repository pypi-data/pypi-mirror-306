import numpy as np
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks


class MgeoModel:
    def __init__(self):
        task = Tasks.sentence_similarity
        model = "damo/mgeo_geographic_entity_alignment_chinese_base"
        self.pipeline_ins = pipeline(task=task, model=model, model_revision='v1.2.0')

    def predict(self, inputs):
        res = self.pipeline_ins(input=inputs)
        sim_label = res["labels"][np.argmax(res["scores"])]
        sim_score = res["scores"][np.argmax(res["scores"])]
        return sim_label, sim_score


mgeo_model = MgeoModel()
