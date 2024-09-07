from django.db import models

#Models for product

class Product(models.Model):
    #for deleting an item, assigning to a value
    LIVE = 1
    DELETE = 0
    #and giving the choice to delete permanent
    DELETE_CHOICES = ((LIVE,'Live'),(DELETE,'Delete'))
    #for title, price, description of the product 
    title = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField()
    #for uploadind the image of the product in the backend 
    #and saved to the media folder
    image = models.ImageField(upload_to='media/')
    #this is to priortize the product which items want to show first
    priority = models.IntegerField(default=0)
    #to check the status weather it is deleted, it set's to defualt LIVE ie:1
    delete_status = models.IntegerField(choices=DELETE_CHOICES,default=LIVE)
    #to update the time in backend while adding a new file and updating
    #the argument is to update date and time automatically
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title