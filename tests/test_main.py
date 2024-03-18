from fastapi.testclient import TestClient

from fastapi_neon.main import app

client = TestClient(app=app)



from fastapi.testclient import TestClient
from  sqlmodel import SQLModel, create_engine, Session
from fastapi_neon.main import app, get_session
from  fastapi_neon.model.model import Todos
from  fastapi_neon  import settings

# client = TestClient(app)




def test_read_main():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}






def test_write_main():
    connection_string = str(settings.TEST_DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg")
    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)
    SQLModel.metadata.create_all(engine)  
    with Session(engine) as session:  
        def get_session_override():  
                return session  
        app.dependency_overrides[get_session] = get_session_override 
        client = TestClient(app=app)
        response = client.post("/todo",json={
                "status":"pending",
                "title":"test_todo_title",
                "description":"test_description"
            },headers={
                 'token':"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InNhbG1hbkBnbWFpbC5jb20iLCJpZCI6MTksImV4cCI6MTcxMDcyMTExNn0.x3NmT7_wk_SNwCZaay1sbfdiHjLAlrK_zZ2iqFGt6mc" 
            }
        )
        data = response.json()
        assert response.status_code == 200
        assert data["title"] == "test_todo_title"








def test_read_list_main():
    connection_string = str(settings.TEST_DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg")
    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)

    SQLModel.metadata.create_all(engine)  

    with Session(engine) as session:  

        def get_session_override():  
                return session  

        app.dependency_overrides[get_session] = get_session_override 
        client = TestClient(app=app)

        response = client.get("/todos",headers={
                 'token':"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InNhbG1hbkBnbWFpbC5jb20iLCJpZCI6MTksImV4cCI6MTcxMDcyMTExNn0.x3NmT7_wk_SNwCZaay1sbfdiHjLAlrK_zZ2iqFGt6mc" 
            })
        assert response.status_code == 200










def test_create_user():
    connection_string = str(settings.TEST_DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg")
    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)

    SQLModel.metadata.create_all(engine)  

    with Session(engine) as session:  

        def get_session_override():  
                return session  

        app.dependency_overrides[get_session] = get_session_override 
        client = TestClient(app=app)
        response = client.post("/signup", json={"first_name": "test_first_name","last_name": "test_last_name","email": "test@gmail.com","password": "string"})
        assert response.status_code == 404
        assert response.json() == {"detail": "Email already in use!"}











def test_login_user_if_not_fond():
    connection_string = str(settings.TEST_DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg")
    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)

    SQLModel.metadata.create_all(engine)  

    with Session(engine) as session:  

        def get_session_override():  
                return session  

        app.dependency_overrides[get_session] = get_session_override 
        client = TestClient(app=app)
        response = client.post("/login", json={"email": "tet@gmail.com","password": "strisng"})
        if response.json() == {"detail": "User not found"}:
            assert response.status_code == 404
            assert response.json() == {"detail": "User not found"}

   









def test_login_user_if_invalid_email_or_password():
    connection_string = str(settings.TEST_DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg")
    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)

    SQLModel.metadata.create_all(engine)  

    with Session(engine) as session:  

        def get_session_override():  
                return session  

        app.dependency_overrides[get_session] = get_session_override 
        client = TestClient(app=app)
        response = client.post("/login", json={"email": "tesadasdst@gmail.com","password": "wrongpass"})
        if response.json() == {"detail": "Invalid email or password!"}:
            assert response.status_code == 404
            assert response.json() == {"detail": "Invalid email or password!"}









def test_login_user_success():
    connection_string = str(settings.TEST_DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg")
    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)

    SQLModel.metadata.create_all(engine)  

    with Session(engine) as session:  

        def get_session_override():  
                return session  

        app.dependency_overrides[get_session] = get_session_override 
        client = TestClient(app=app)
        response = client.post("/login", json={"email": "tesadasdst@gmail.com","password": "string"})
        assert response.status_code == 200
        assert response.json().get("token_type") == "bearer"
