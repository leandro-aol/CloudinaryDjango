from django.contrib import admin
from .models import Items


class ItemsAdmin(admin.ModelAdmin):

    list_display = ['id', 'name', 'category', 'comment']    # Define as colunas que aparecerão na exibição dos dados no admin
    search_fields = ['name', 'comment']                     # Acrescenta uma barra de pesquisa que permite a busca pelo(s) campo(s) definido(s)
    readonly_fields = ['imageURL']                             # Durante a edição o(s) campo(s) será(ão) somente para leitura
    exclude = ['imageFile']                                 # Remove o(s) campo(s) do formulário de edição do registro
    list_filter = ['category']                              # Acrescenta a possibilidade de filtrar de acordo com o(s) campo(s) escolhido(s)

admin.site.register(Items, ItemsAdmin)  # Add a model in admin
