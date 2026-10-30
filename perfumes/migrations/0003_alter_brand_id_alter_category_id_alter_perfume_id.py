from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfumes', '0002_alter_brand_id_alter_category_id_alter_perfume_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='perfume',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
