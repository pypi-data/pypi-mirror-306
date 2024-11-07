from django.db import models


class DdosSettings(models.Model):
    timeout = models.PositiveIntegerField(default=5 * 60)
    max_requests = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"Max Requests: {self.max_requests}, Block Time: {self.timeout} seconds"
