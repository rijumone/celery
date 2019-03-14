# get_from_q_process.py

import json
import datetime

# Setting up SQLAlchemy

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql://decisiontree:decisiontree123@decision-tree.cxhedmomc3jg.us-east-1.rds.amazonaws.com/dc_cust', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class RequestsModel(Base):
	__tablename__ = 'wh_requests'
	
	id = Column(Integer, primary_key=True)
	request = Column(String(4294967295))
	created_at = Column(DateTime, default=datetime.datetime.utcnow)

	def __repr__(self):
		return "<Requests(id={id}, request={request}, created_at={created_at})>".format(
			id=id,
			request=request,
			created_at=created_at,
			)

# Setting up Celery
from celery import Celery

app = Celery('get_from_q_process', 
	broker='amqp://localhost//', 
	backend='db+mysql://decisiontree:decisiontree123@decision-tree.cxhedmomc3jg.us-east-1.rds.amazonaws.com/dc_playground')

# adding tasks
@app.task
def load(request):
	try:
		request = RequestsModel(request=json.dumps(request))
		session.add(request)
		session.commit()
		return True
	except Exception as e:
		print(e)
		return False