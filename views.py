

from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views.generic import ListView, DetailView
# from .forms import ProductForm, ProductModeratorForm
# from .models import Product, Category
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
# from catalog.servies import get_product_from_cache, get_product_category


class SendingtListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):  # подключаем к представлению функцию обращения к кешу
        return get_product_from_cache()

    def get_queryset(self):
        user = self.request.user
        if user.has_perm("catalog.can_unpublish_product"):
            return Product.objects.all()
        elif not user.is_authenticated:
            return Product.objects.filter(is_published=True)
        else:
            return Product.objects.filter(owner=user)
    # success_url = reverse_lazy('catalog:catalog/product_list')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    # def get_object(self, queryset=None):     # функция, которая показывает карточку товара только его владельцу
    #     self.object = super().get_object(queryset)
    #     if self.queryset == self.object.owner:
    #         self.object.save()
    #         return self.object
    #     raise PermissionDenied


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_create.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm("catalog.can_unpublish_product"):
            return ProductModeratorForm
        raise PermissionDenied

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')


class ProductServiceView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'catalog/product_list_from_category.html'
    context_object_name = 'products_category'

    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        return get_product_category(category_id=category_id)

#
#
# def home(request):
#     return render(request, 'catalog/home.html')
#
# def contacts(request):
#     return render(request, 'catalog/contacts.html')
#
# def base(request):
#     return render(request, 'catalog/base.html')

# def products_list(request):
#     products = Product.objects.all()
#     context = {"products": products}
#     return render(request,'catalog/products_list.html', context)

# def product_detail(request, pk):
#     # product = Product.objects.get(pk=pk)
#     product = get_object_or_404(Product, pk=pk)
#     context = {'product': product}
#     return render(request, 'catalog/product_detail.html', context)

# def contact_data(request):
#     if request.method == 'POST':
#         # Получение данных из формы
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#         # Обработка данных (например, сохранение в БД, отправка email и т. д.)
#         # Здесь мы просто возвращаем простой ответ
#         return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
#     return render(request, 'catalog/contacts.html')