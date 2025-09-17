from locust import HttpUser, task

class APIUser(HttpUser):
    @task
    def health(self):
        self.client.get('/')
