from . import Base
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from datetime import datetime

class ScriptRun(Base):
    __tablename__ = 'script_runs'

    id = Column(Integer, primary_key=True)
    script_id = Column(Integer, ForeignKey("check_scripts.id"))
    exit_code = Column(Integer)
    output = Column(Text(20000000))
    date = Column(DateTime, default=datetime.utcnow())

    def to_dict(self) -> dict:
        return {
            'exit_code': self.exit_code,
            'output': self.output,
            'date': self.date
        }
