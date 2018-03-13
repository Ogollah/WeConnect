class Review:
    class_counter = 1

    def __init__(self, review, business_id):
        self.review = review
        self.business_id = business_id
        self.review_id = Review.class_counter
        Review.class_counter += 1
