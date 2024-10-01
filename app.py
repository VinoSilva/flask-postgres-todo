from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields,marshal_with,abort
import os
from dotenv import load_dotenv

load_dotenv()

# Organizing files
# Next part is authentication

app = Flask(__name__)
database_url = os.getenv("DATABASE_URL")
print(database_url)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
db = SQLAlchemy(app)

# db.create_all()
api = Api(app)

todo_args = reqparse.RequestParser()
todo_args.add_argument('content',type=str,required=True,help='Content cannot be blank')

todoFields = {
    'id': fields.Integer,
    'content': fields.String
}

class TodoModel(db.Model):
    # __tablename__ = 'todos'
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(80),nullable=False)
    
    def __repr__(self):
        return f"Todo(id = {self.id},content = {self.content})"
    
class Todos(Resource):
    @marshal_with(todoFields)
    def get(self):
        todos = TodoModel.query.all()
        return todos
    
    @marshal_with(todoFields)
    def post(self):
        args = todo_args.parse_args()
        todo = TodoModel(content=args["content"])
        db.session.add(todo)
        db.session.commit()
        todos = TodoModel.query.all()
        return todos, 201

class Todo(Resource):
    @marshal_with(todoFields)
    def get(self,id):
        todo = TodoModel.query.filter_by(id=id).first()
        if not todo:
            abort(404,message="Todo not found")
        return todo
    
    @marshal_with(todoFields)
    def patch(self,id):
        todo = TodoModel.query.filter_by(id=id).first()
        args = todo_args.parse_args()
        if not todo:
            abort(404,message="Todo not found")
        todo.content = args["content"]
        db.session.commit()
        return todo
    
    @marshal_with(todoFields)
    def delete(self,id):
        todo = TodoModel.query.filter_by(id=id).first()
        if not todo:
            abort(404,message="Todo not found")
        db.session.delete(todo)
        db.session.commit();
        todos = TodoModel.query.all();
        # return todos, 204;
        return todos, 200;

api.add_resource(Todos,'/api/todos')
api.add_resource(Todo, '/api/todos/<int:id>')

# @app.route('/')
# def home():
#     return "Hello, Flask!"

if __name__ == '__main__':
    app.run()