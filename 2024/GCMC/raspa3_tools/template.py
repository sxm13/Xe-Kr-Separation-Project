import json

DEFAULT_SETTINGS = {
                    "SimulationType": "MonteCarlo",
                    "NumberOfCycles": 20000,
                    "NumberOfInitializationCycles": 10000,
                    "PrintEvery": 5000,
                    "ForceField": ".",
                    "Type" : "Framework",
                    "CIFName" : "example",
                    "CutOff" : 12,
                    "NumberOfUnitCells" : [1,1,1],
                    "ExternalTemperature" : 298,
                    "ExternalPressure" : 1.0e5,
                    "ChargeMethod" : "None",
                    "task": "SingleAdsorption",
                    "MolName": ["Xe"],
                    "MolFrac": [0.2,0.8],
                    "MoleculeDefinition": ".",
                    "idealGasRosenbluthWeight": 1,
                    "FugacityCoefficient": 1,
                    "TranslationProbability": 1.0,
                    "RotationProbability": 1.0,
                    "ReinsertionProbability": 1.0,
                    "SwapProbability": 1.0,
                    "CreateNumberOfMolecules": 0
                    }


class Generate:
    
    def __init__(self, **kwargs):
        config = DEFAULT_SETTINGS.copy()
        config.update(kwargs)
        for key, value in config.items():
            setattr(self, key, value)

    def to_dict(self):
        if self.task == "SingleAdsorption":
            return {
                "SimulationType": self.SimulationType,
                "NumberOfCycles": self.NumberOfCycles,
                "NumberOfInitializationCycles": self.NumberOfInitializationCycles,
                "PrintEvery": self.PrintEvery,
                "ForceField": self.ForceField,
                "Systems" : [
                    {
                    "Type": self.Type,
                    "Name": self.CIFName,
                    "CutOff": self.CutOff,
                    "NumberOfUnitCells": self.NumberOfUnitCells,
                    "ExternalTemperature": self.ExternalTemperature,
                    "ExternalPressure": self.ExternalPressure,
                    "ChargeMethod": self.ChargeMethod
                    }
                    ],
                "Components" : [
                    {
                    "Name": self.MolName,
                    "MoleculeDefinition": self.MoleculeDefinition,
                    "idealGasRosenbluthWeight": self.idealGasRosenbluthWeight,
                    "FugacityCoefficient": self.FugacityCoefficient,
                    "TranslationProbability": self.TranslationProbability,
                    "RotationProbability": self.RotationProbability,
                    "ReinsertionProbability": self.ReinsertionProbability,
                    "SwapProbability": self.SwapProbability,
                    "CreateNumberOfMolecules": self.CreateNumberOfMolecules,
                    }
                ]
            }
        elif self.task == "MixtureAdsorption":
            return {
                "SimulationType": self.SimulationType,
                "NumberOfCycles": self.NumberOfCycles,
                "NumberOfInitializationCycles": self.NumberOfInitializationCycles,
                "PrintEvery": self.PrintEvery,
                "ForceField": self.ForceField,
                "Systems": [
                    {
                        "Type": self.Type,
                        "Name": self.CIFName,
                        "CutOff": self.CutOff,
                        "NumberOfUnitCells": self.NumberOfUnitCells,
                        "ExternalTemperature": self.ExternalTemperature,
                        "ExternalPressure": self.ExternalPressure,
                        "ChargeMethod": self.ChargeMethod
                    }
                ],
                "Components": [
                    {
                        "Name": mol_name,
                        "MolFraction": mol_fraction,
                        "MoleculeDefinition": self.MoleculeDefinition,
                        "idealGasRosenbluthWeight": self.idealGasRosenbluthWeight,
                        "FugacityCoefficient": self.FugacityCoefficient,
                        "TranslationProbability": self.TranslationProbability,
                        "RotationProbability": self.RotationProbability,
                        "ReinsertionProbability": self.ReinsertionProbability,
                        "SwapProbability": self.SwapProbability,
                        "CreateNumberOfMolecules": self.CreateNumberOfMolecules
                    }
                    for mol_name, mol_fraction in zip(self.MolName, self.MolFrac)
                ]
            }


    def save_to_json(self, filename):
        with open(filename, "w") as f:
            json.dump(self.to_dict(), f, indent=4)
    
    def __call__(self):
        return self.to_dict()

    def __repr__(self):
        return str(self.to_dict())
    