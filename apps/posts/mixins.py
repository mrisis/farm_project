

class ImageUrlMixin:

    def get_image_url(self, instance, image_field='profile_image', default=None):

        image = getattr(instance, image_field, None)
        if not image:
            return default

        if hasattr(image, 'image') and hasattr(image.image, 'url'):
            return self.context['request'].build_absolute_uri(image.image.url)
        elif hasattr(image, 'url'):
            return self.context['request'].build_absolute_uri(image.url)
        
        return default
