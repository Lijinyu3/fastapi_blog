from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas
from . import models
from blog.database import engine, SessionLocal
from sqlalchemy.orm import session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
# method for create a blog
def create_blog(request: schemas.Blog, db: session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog')
# method for get all blogs
def get_all(db: session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=status.HTTP_200_OK)
# method for get a blog
def show_blog(id, db: session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'blog with the id {id} is not found')
    return blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
# method for delete a blog
def delete_blog(id, db: session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id ==
                                 id).delete(synchronize_session=False)
    db.commit()
    return f'blog with the id {id} is deleted!'
