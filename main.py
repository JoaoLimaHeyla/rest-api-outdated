#O request como objeto pode ser usado em Resource para nos 
# dar info dos dados que são feitos por uma requisição
from flask import Flask, abort, make_response #, request

#banco sql famoso para flask
from flask_sqlalchemy import SQLAlchemy
#outdated, o Flask atual já pode ser usado sozinho
#sem precisar do import do flask_restful
#O reqparse faz com que ao enviar uma requisição, 
# você precise passar a info que precisa para essa req
from flask_restful import Api, Resource, reqparse, fields, marshal_with

app = Flask(__name__)
api = Api(app)
#para criar db e tbm seu destino (nesse caso é direto nessa pasta)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#Basicamente criando uma table
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={name}, views={views}, likes={likes})"

#deixa aqui para a primeira vez que criar, e depois tira 
# para não substituir o nosso db para criar outro 
#db.create_all()

#analisa a classe que ele estiver e se tem a info correta
video_put_args = reqparse.RequestParser()
#Esses são os argumentos necessários para passar pelo ReqParser
#Necessário ter o required
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video is required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of the video is required", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video is required")
video_update_args.add_argument("likes", type=int, help="Likes of the video is required")


#*********Não é necessário após colocar o SQLAlchemy*********
#Para evitar o crash do servidor
# def abort_if_video_id_doesnt_exist(video_id):
#     if video_id not in videos:
#         abort(404, "Video not found")

# def abort_if_video_id_exists(video_id):
#     if video_id in videos:
#         abort(409, "Video already exists with that ID")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views':fields.Integer,
    'likes':fields.Integer
}

#Resource tem métodos para que possamos substituir(override),
#ajudando a lidar com requisições GET POST PUT DELETE...
class Video(Resource):

    #O marshal_with pega o return e serializa de acordo
    #com a variável JSON
    @marshal_with(resource_fields)
    def get(self, video_id):
        #Caso o vídeo não exista
        #abort_if_video_id_doesnt_exist(video_id)
        
        #o first() pega o primeiro daquele valor
        #ex: se eu quisesse trazer um vídeo com 10 views qualquer,
        #  eu apenas preciso colocar first que ele me trará o primeiro  
        result = VideoModel.query.filter_by(id= video_id).first()
        if not result:
            abort(404, "Video not found")
        return result
    
    
    @marshal_with(resource_fields)
    def put(self, video_id):
        #Caso o vídeo exista
        #abort_if_video_id_exists(video_id)
        
        #verifica os argumentos mandatórios name,views,likes
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id= video_id).first()
        if result:
            abort(409, "Video ID taken")

        video = VideoModel(id= video_id, name=args['name'], views=args['views'], likes=args['likes'])
        #adiciona temporariamente
        db.session.add(video)
        #adiciona de vez
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id ):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id= video_id).first()
        if not result:
            abort(404, "Video not found, can't update")

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']
        
        db.session.commit()

        return result, 200
        
    def delete(self, video_id):
        #abort_if_video_id_doesnt_exist(video_id)
        
        return 'Video deleted successfully', 204

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    #o debug=True é para ver a info/logs
    #não use em produção, apenas em desenvolvimento
    app.run(debug=True)