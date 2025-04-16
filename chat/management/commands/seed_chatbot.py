from django.core.management.base import BaseCommand
from chat.models import BotResponse


class Command(BaseCommand):
    help = 'Seeds the database with initial chatbot responses'

    def handle(self, *args, **options):
        # Clear existing responses
        BotResponse.objects.all().delete()

        # Create predefined responses
        responses = [
            # Greetings
            {
                'category': 'greeting',
                'keywords': 'hello,hi,hey,greetings',
                'response_text': 'Hello! Welcome to Floral Couture. How can I assist you today?',
                'priority': 1
            },
            {
                'category': 'greeting',
                'keywords': 'good morning,good afternoon,good evening',
                'response_text': 'Good day! How can I help you with your floral needs?',
                'priority': 1
            },
            # Product inquiries
            {
                'category': 'product',
                'keywords': 'rose,roses,flower,flowers',
                'response_text': 'We have a beautiful selection of roses and other flowers! You can browse our collection on the Bouquets page or design your own arrangement.',
                'priority': 2
            },
            {
                'category': 'product',
                'keywords': 'bouquet,arrangement,design',
                'response_text': 'Our bouquets are handcrafted with care. You can browse pre-made arrangements or create your custom bouquet with your favorite flowers!',
                'priority': 2
            },
            # Delivery
            {
                'category': 'delivery',
                'keywords': 'delivery,shipping,deliver,ship,time',
                'response_text': 'We offer same-day delivery for orders placed before 2pm, and next-day delivery for later orders. You can select your preferred delivery date at checkout.',
                'priority': 2
            },
            # Orders
            {
                'category': 'order',
                'keywords': 'order,status,tracking',
                'response_text': 'To check your order status, please log in to your account and visit the Orders section. If you have any specific concerns, please provide your order number.',
                'priority': 2
            },
            # Custom bouquets
            {
                'category': 'custom',
                'keywords': 'custom,personalize,customize,special',
                'response_text': 'Our custom bouquet service allows you to choose your flowers, colors, and arrangement style. Visit our Customize page to create your perfect arrangement!',
                'priority': 3
            },
            # Farewells
            {
                'category': 'farewell',
                'keywords': 'bye,goodbye,thanks,thank you',
                'response_text': 'Thank you for chatting with us! If you need anything else, feel free to reach out. Have a wonderful day!',
                'priority': 1
            },
            # Fallbacks
            {
                'category': 'fallback',
                'keywords': 'help,support,confused,dont understand',
                'response_text': "I'm here to help! You can ask about our bouquets, delivery options, or custom arrangements. If you need to speak with a human, please use our Contact page.",
                'priority': 1
            },
        ]

        for response_data in responses:
            BotResponse.objects.create(**response_data)

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {len(responses)} chatbot responses'))
