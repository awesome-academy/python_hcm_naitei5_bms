from django.db import models

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    firts_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_staff = models.BooleanField()
    is_usersupper = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    is_active = models.BooleanField(default= True)
    activation_token = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.is_active}"

class Tour(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    #average_rating = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name
    def calculate_average_rating(self):
            # Lấy tất cả các đánh giá của tour du lịch
        ratings = Rating.objects.filter(tour=self)

        # Tính tổng các đánh giá
        total_ratings = sum(rating.value for rating in ratings)

        # Kiểm tra nếu không có đánh giá nào, tránh chia cho 0
        if not ratings.exists():
            return 0

        # Tính trung bình các đánh giá
        average = total_ratings / len(ratings)

        # Làm tròn kết quả đến 2 chữ số thập phân
        return round(average, 2)

class Image(models.Model):
    id = models.IntegerField(primary_key=True)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='tour_images/')

    def __str__(self):
        return f"Image {self.id} for Tour {self.tour.name}"

class Booking(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    #tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add= True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_people = models.CharField(max_length=255)
    departure_date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.tour.name} - {self.status}"

class Rating(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    rating = models.IntegerField()
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"{self.user.username} - {self.tour.name} - {self.rating}"
        