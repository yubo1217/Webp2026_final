from rest_framework import generics, viewsets, status
from django.http import FileResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Folder, File
from .serializers import RegisterSerializer, UserSerializer, FolderSerializer, FileSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': UserSerializer(user).data})
    return Response({'error': '帳號或密碼錯誤'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_view(request):
    try:
        request.user.auth_token.delete()
    except Exception:
        pass
    return Response({'message': '已登出'})


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class FolderViewSet(viewsets.ModelViewSet):
    serializer_class = FolderSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Folder.objects.filter(user=user)
        if self.action == 'list':
            parent = self.request.query_params.get('parent', None)
            if parent == 'null' or parent is None:
                qs = qs.filter(parent=None)
            else:
                qs = qs.filter(parent_id=parent)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer

    def get_queryset(self):
        user = self.request.user
        qs = File.objects.filter(user=user)
        if self.action == 'list':
            folder = self.request.query_params.get('folder', None)
            if folder == 'null' or folder is None:
                qs = qs.filter(folder=None)
            else:
                qs = qs.filter(folder_id=folder)
        return qs

    def get_serializer_context(self):
        return {'request': self.request}

    def create(self, request, *args, **kwargs):
        uploaded = request.FILES.get('file')
        if not uploaded:
            return Response({'error': '沒有收到檔案'}, status=status.HTTP_400_BAD_REQUEST)

        folder_id = request.data.get('folder') or None
        folder = None
        if folder_id:
            try:
                folder = Folder.objects.get(id=folder_id, user=request.user)
            except Folder.DoesNotExist:
                return Response({'error': '資料夾不存在'}, status=status.HTTP_404_NOT_FOUND)

        existing = File.objects.filter(
            name=uploaded.name, user=request.user, folder=folder
        ).first()
        if existing:
            existing.file.delete(save=False)
            existing.file = uploaded
            existing.size = uploaded.size
            existing.mime_type = uploaded.content_type
            existing.save()
            serializer = self.get_serializer(existing)
        else:
            file_obj = File.objects.create(
                name=uploaded.name,
                file=uploaded,
                size=uploaded.size,
                mime_type=uploaded.content_type,
                folder=folder,
                user=request.user,
            )
            serializer = self.get_serializer(file_obj)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def download(self, request, *args, **kwargs):
        instance = self.get_object()
        response = FileResponse(instance.file.open('rb'), content_type=instance.mime_type or 'application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{instance.name}"'
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.file.delete(save=False)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
