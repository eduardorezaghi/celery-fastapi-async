from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//', backend='redis://localhost')

@app.task
def add_product(name, category_id, price):
    # Implement logic to add a product to the database
    pass