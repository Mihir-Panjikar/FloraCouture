from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from django.contrib.auth.models import AnonymousUser
from .models import Order
from .serializers import OrderSerializer

# 1️⃣ Create Order API
class OrderCreateView(APIView):
    def post(self, request):
        # Copy request data to make it mutable
        data = request.data.copy()
        
        # Handle user authentication
        if request.user and not isinstance(request.user, AnonymousUser):
            data['user'] = request.user.id
        else:
            # For guest checkout, you might want to handle this differently
            return Response({"error": "User authentication required"}, 
                           status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            order = serializer.save()
            return Response({
                "success": True,
                "order_id": order.id,
                "message": "Order created successfully"
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2️⃣ Retrieve Order Details API
class RetrieveOrderView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


# 3️⃣ Update Order Status API
class UpdateOrderStatusView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        new_status = request.data.get("status")
        if new_status:
            order.status = new_status
            order.save()
            return Response({"message": "Order status updated successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Status field is required"}, status=status.HTTP_400_BAD_REQUEST)


# 4️⃣ List Orders for Retailers/Customers API
class ListOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        # Check if this user has any orders as a retailer
        retailer_orders = Order.objects.filter(retailer=user)
        if retailer_orders.exists():
            return retailer_orders
        # Otherwise return customer orders
        return Order.objects.filter(customer=user)


# 5️⃣ Cancel Order API
class CancelOrderView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def delete(self, request, *args, **kwargs):
        order = self.get_object()
        if order.status == "Pending":
            order.delete()
            return Response({"message": "Order cancelled successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Cannot cancel an order that is not pending"}, status=status.HTTP_400_BAD_REQUEST)
