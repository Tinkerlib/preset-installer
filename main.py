import bpy
from pathlib import Path
import os
import shutil
import pprint

class PresetManager():


    def __init__(self):
        self.update_data()


    def update_data(self):

        self.source_path = os.path.join(os.path.dirname(__file__), "source")
        self.operator_presets = {}
        source_operator_ids = os.listdir(self.source_path)
    
        for operator_id in source_operator_ids:
            operator_preset = OperatorPreset(operator_id, self.source_path)
            self.operator_presets[operator_id] = operator_preset


    
    def install(self):
        for op in self.operator_presets.values():
            op.install()
            



class OperatorPreset():

    def __init__(self, id, source_path):
        self.id = id
        self.source_folder = source_path
        self.target_folder = os.path.join(bpy.utils.script_path_user(), "presets", "operator")
        self.target_path = os.path.join(self.target_folder, self.id)
        
        self.source_path = os.path.join(self.source_folder, id)
        self.presets = {}

        for preset_name in os.listdir(self.source_path):
            self.presets[preset_name] = PresetItem(self.source_path, self.target_path, preset_name, self.id)

    def __repr__(self):
        return f"\n OperatorPreset(\n \t id: {self.id},\n \t path: {self.source_path}, \n \t presets: {list(self.presets.keys())}\n\t)"

    def ensure_folder(self):
        if not os.path.exists(self.target_path):
            os.makedirs(self.target_path)

    def install(self, force):
        self.ensure_folder()
        for preset in self.presets.values():
            preset.install()


class PresetItem():
    def __init__(self, source_folder, target_folder, name, operator_id):

        self.name = name
        self.source_folder = source_folder
        self.target_folder = target_folder
        self.operator_id = operator_id
        
        self.target_path = os.path.join(self.target_folder, name)
        self.source_path = os.path.join(self.source_folder, name)

    def exist(self):
        return os.path.exists(self.target_path)
    
    def install(self):
        if not self.exist():
            print(f"Installed {self.name} Preset for {self.operator_id}")
            shutil.copy2(self.source_path, self.target_path)


    def __repr__(self):
        return f"\n PresetItem(\n \t name: {self.name} \n\t)"



def register():
    preset_manager = PresetManager()
    preset_manager.install()


def unregister():
    pass

if __name__ == "__main__":
    register()
