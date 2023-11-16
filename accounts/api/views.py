from rest_framework.response import Response
from django.http import JsonResponse

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.decorators import api_view 
from accounts.api.serializers import SignupSerializer,LoginSerializer,UserModelSerializer,profileupdateSerializer,CustomUserSerializer,PartnerModelSerializer,WalletSerializer
from rest_framework import status
from accounts.models import UserProfile,PartnerProfile,CustomUser,Wallet
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken




import datetime
class UserLoginView(APIView):
    def post(self, request):
        print("hi----------------")
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                email = 'user-' + serializer.data['email']  # Prefix with 'user-'
                password = serializer.data['password']
                print("email",email)
                user = authenticate(email=email, password=password)
                
                if user is None or user.role != 'user' or user.is_blocked:
                    data = {
                        'message': 'Invalid credentials or user is blocked.',
                    }
                    print("data",data)
                    return Response(data, status=status.HTTP_400_BAD_REQUEST) 
                
                refresh = RefreshToken.for_user(user)
                # refresh['role'] = user.role
                # refresh['email'] = user.email
                # refresh['username'] = user.username
                # refresh['phone_no'] = user.phone_no
                # refresh['profile_photo'] = user.profile_photo
                # refresh['is_superuser'] = user.is_superuser
                
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    # 'username':user.username,
                    # 'phone_no':user.phone_no,
                    # 'profile_photo':profile_photo,
                }
                print("Serialized Data:", data)
                return Response(data, status=status.HTTP_200_OK)
            
            return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': serializer.errors
            })

        except Exception as e:
            print(e)

class PartnerLoginView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            
            if serializer.is_valid():
                email = 'partner-' + serializer.data['email']  # Prefix with 'partner-'
                password = serializer.data['password']
                
                user = authenticate(email=email, password=password)
                print("user",user)
                if user is None or user.role != 'partner' :
                    data = {
                        'message': 'invalid credentials',
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
                
                refresh = RefreshToken.for_user(user)
                refresh['role'] = user.role
                refresh['email'] = user.email
                refresh['partnername'] = user.username
                
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    
                }
                return Response(data, status=status.HTTP_200_OK)
            
            return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': serializer.errors
            })

        except Exception as e:
            print(e)

class AdminLoginView(APIView):
    def post(self, request):
        try:
            data = request.data
            # if data.email==is_superuser
            serializer = LoginSerializer(data=data)
            
            if serializer.is_valid() :
                email =   serializer.data['email']  # Prefix with 'partner-'
                password = serializer.data['password']
                print("usemailer",email)
                user = authenticate(email=email, password=password)
                print("user",user)
                if user is None or user.role != 'admin':
                    data = {
                        'message': 'invalid credentials',
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
                
                refresh = RefreshToken.for_user(user)
                refresh['role'] = user.role
                refresh['email'] = user.email
                refresh['adminname'] = user.username
                
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    
                }
                return Response(data, status=status.HTTP_200_OK)
            
            return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': serializer.errors
            })

        except Exception as e:
            print(e)

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Add custom claims
#         token['username'] = user.username
#         token['is_superuser'] = user.is_superuser

#         return token

#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')

#         # Try to find the user in UserProfile
#         try:
#             user = UserProfile.objects.get(email=email)
#         except UserProfile.DoesNotExist:
#             user = None

#         # If the user doesn't exist in UserProfile, try finding in PartnerProfile
#         if not user:
#             try:
#                 user = PartnerProfile.objects.get(email=email)
#             except PartnerProfile.DoesNotExist:
#                 raise serializers.ValidationError("User with this email does not exist.")

#         if not user.check_password(password):
#             raise serializers.ValidationError("Invalid password.")

#         # Continue with token generation
#         data = super().validate(attrs)
#         refresh = self.get_token(user)
#         data['refresh'] = str(refresh)
#         data['access'] = str(refresh.access_token)

#         return data
# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class=MyTokenObtainPairSerializer  
@api_view(['GET'])
def getRoutes(request):
    routes=[
        '/api/token',
        # '/api/token/refresh'
    ]
    return Response(routes)


# class UserLoginView(APIView):
#      def post(self, request):
#         data = request.data
#         if 'email' not in data or 'password' not in data:
           
#             return Response({'error': 'Both email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

#         email = data['email']
#         password = data['password']
#         user = UserProfile.objects.filter(email=email).first()

#         if not user:
#             raise AuthenticationFailed('User not found!')

#         if not user.check_password(password):
#             raise AuthenticationFailed('Incorrect password!')
        
#         # if not user.is_superuser:
#         #     raise AuthenticationFailed('Access denied!')
        
        
#         payload = {
#             'id': user.id,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#             'iat': datetime.datetime.utcnow(),
#             'is_superuser':is_superuser
#         }
        
#         tocken = jwt.encode(payload, 'secret', algorithm ='HS256')
#         responce = Response()
        
        
        
#         responce.data = {
#                 'jwt': tocken
#             }
        
#         return responce

# class otpverifyAPI(APIView):
#     def post(self,request,pin):
#         pass
    



class UserSignupAPI(APIView):
    def post(self,request):
        print(request.data,"fffffffffffffffffffffff")
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            # user = serializer.save()
            print(user_data,"ser_data")
            user = CustomUser(
                
                
                email = 'user-' + user_data['email'],
                
                
                role = 'user',
                phone_no = 'user-' + user_data['phone_no'],
                username = user_data['username'],
            )

            user.set_password(user_data['password'] )
            user.save()

            UserProfile.objects.create(user=user)
            return Response({'message':'Account created successfully.'},status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



         
class PartnerSignupAPI(APIView):
    def post(self,request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            # user = serializer.save()
           
            user = CustomUser(
                username = user_data['username'],
                
                email = 'partner-' + user_data['email'],
                phone_no = 'partner-' + user_data['phone_no'],
                role = 'partner'
            )

            user.set_password(user_data['password'] )
            user.save()

            PartnerProfile.objects.create(user=user)
            print('partner is created ')
            return Response({'message':'Account created successfully.'},status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])        
def userlist(request):
    if request.method == 'GET':
        
        data = UserProfile.objects.all()
        
        serializer = UserModelSerializer(data, many=True)
        # print("ggggggggggggggggggggg",data,'kkkkkkkkkkkkkkkk',serializer.data)
        
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['GET'])        
def userblock(request,user_id):
    print("id",user_id)
    if request.method == 'GET':
        user_profile = CustomUser.objects.get(id=user_id)
        
        print("ggggggggg")
        user_profile.is_blocked = not user_profile.is_blocked
             
        user_profile.save()      
        print("user_profile.is_blocked------------------->",user_profile.is_blocked)    
        return Response({'message':'Account Modified successfully.'},status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['POST'])
def profileupdate(request, user_id):
    print("request.data",request.data)
    try:
        user_profile = CustomUser.objects.get(id=user_id)
        
    except CustomUser.DoesNotExist:
        return Response({'message': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    print("userprofile",user_profile)  
    print("data----------------------------------",request.data)  
    serializer = profileupdateSerializer(data=request.data, instance=user_profile, partial=True)
    print("serializer",serializer)
    if serializer.is_valid():
        print("hhhhhhh")
        user_data = serializer.validated_data
        print("data",user_data) 
        if request.method=='POST': 
            if 'username' in request.data:
               user_profile.username = user_data.get('username', user_profile.username)
            if 'phone_no' in request.data:   
                user_profile.phone_no = user_data.get('phone_no', user_profile.phone_no)
            if 'profile_photo' in request.data:   
                user_profile.profile_photo = user_data.get('profile_photo', user_profile.profile_photo)    
       
        user_profile.save()
        return Response({'message': 'Accounts updated successfully.'}, status=status.HTTP_201_CREATED)
    if not serializer.is_valid():
       print(serializer.errors)
    
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])        
def userprofile(request, user_id):
    print("id", user_id)
    if request.method == 'GET':
        
            user = CustomUser.objects.get(id=user_id)
            print("user",user)
            serializer = CustomUserSerializer(user)  # Pass 'user' as a keyword argument
            print("serializer",serializer.data)

            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])        
def Partnerprofile(request, user_id):
    print("id", user_id)
    if request.method == 'GET':
            print("idd",user_id)
        
            user = PartnerProfile.objects.get(user=user_id)
            # partner_profile = PartnerProfile(user=user)
            print("user-------------------",user)
            serializer = PartnerModelSerializer(user)  # Pass 'user' as a keyword argument
            print("serializer-------------------",serializer.data)

            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class Walletmoney(APIView):
    def get(self,request,*args,**kwargs):
        user_id=self.kwargs.get('user_id')
        user = CustomUser.objects.get(id=user_id)
        user_profile=UserProfile.objects.get(user=user)
        
        wallet = Wallet.objects.get(user=user_profile)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)