from torch import nn
from ssd.modeling.backbone.vgg import VGG
from ssd.modeling.backbone.basic import BasicModel
from ssd.modeling.backbone.ResNet import ResNet
from ssd.modeling.backbone.MobileNet import MobileNet
from ssd.modeling.backbone.ResNet50 import ResNet50
from ssd.modeling.backbone.ResNet50_v2 import ResNet50_v2
from ssd.modeling.backbone.Inception import Inception
from ssd.modeling.backbone.ResNext import ResNext
from ssd.modeling.box_head.box_head import SSDBoxHead
from ssd.utils.model_zoo import load_state_dict_from_url
from ssd import torch_utils


class SSDDetector(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.backbone = build_backbone(cfg)
        self.box_head = SSDBoxHead(cfg)
        print(
            "Detector initialized. Total Number of params: ",
            f"{torch_utils.format_params(self)}")
        print(
            f"Backbone number of parameters: {torch_utils.format_params(self.backbone)}")
        print(
            f"SSD Head number of parameters: {torch_utils.format_params(self.box_head)}")

    def forward(self, images, targets=None):
        features = self.backbone(images)
        detections, detector_losses = self.box_head(features, targets)
        if self.training:
            return detector_losses
        return detections


def build_backbone(cfg):
    backbone_name = cfg.MODEL.BACKBONE.NAME
    
    if backbone_name == "Inception":
        model = Inception(cfg)
        return model
    
    if backbone_name == "basic":
        model = BasicModel(cfg)
        return model
    
    if backbone_name == "MobileNet":
        model = MobileNet(cfg)
        return model
    
    if backbone_name == "ResNet50":
        model = ResNet50(cfg)
        return model
    
    
    if backbone_name == "ResNet":
        model = ResNet(cfg) 
        return model
    
    if backbone_name == "ResNet50_v2":
        model = ResNet50_v2(cfg)
        return model
    
    if backbone_name == "ResNext":
        model = ResNext(cfg)
        return model
    
    if backbone_name == "vgg":
        model = VGG(cfg)
        if cfg.MODEL.BACKBONE.PRETRAINED:
            state_dict = load_state_dict_from_url(
                "https://s3.amazonaws.com/amdegroot-models/vgg16_reducedfc.pth")
            model.init_from_pretrain(state_dict)
        return model
