from . import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

class CheckScript(Base):
    __tablename__ = 'check_scripts'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True)
    script = Column(Text(200000))
    script_runs = relationship('ScriptRun')
    schedule = Column(String(64), default="0 * * * *")

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'script': self.script,
            'script_runs': [
                sr.to_dict() for sr in self.script_runs
            ]
        }

    @staticmethod
    def from_dict(data: dict):
        cs = CheckScript()
        cs.id = data['id'] if 'id' in data else None
        cs.name = data['name']
        cs.script = data['script']
        cs.schedule = data['schedule']
        cs.script_runs = data['script_runs'] if 'script_runs' in data else []
        return cs
