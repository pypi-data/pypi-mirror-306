from setuptools import setup, find_packages

setup(
    name="alphabet_of_languages",  # نام کتابخانه
    version="0.1.2",               # نسخه اولیه (با آپدیت کتابخانه، این عدد تغییر می‌کند)
    author="ParsaPouramiri",            # نام شما
    author_email="pouramiriparsa@gmail.com",  # ایمیل شما
    description="A simple library providing Persian and English alphabets",  # توضیح کوتاه درباره کتابخانه
    long_description=open("README.md").read(),  # توضیح کامل از فایل README.md
    long_description_content_type="text/markdown",  # نوع محتوای توضیحات طولانی
    url="https://github.com/username/alphabet_of_languages",  # لینک به مخزن (مثلاً GitHub)
    packages=find_packages(),  # شامل تمام بسته‌ها (پوشه‌های حاوی `__init__.py`)
    classifiers=[               # دسته‌بندی‌ها برای کمک به یافتن کتابخانه شما
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",    # نسخه پایتون مورد نیاز
)