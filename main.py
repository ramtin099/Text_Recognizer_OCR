import cv2
import easyocr
from spellchecker import SpellChecker


# 1. تابع برای استخراج متن با EasyOCR
def extract_text_with_easyocr(image):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image)
    extracted_text = [text[1] for text in result]  # فقط متن‌ها رو می‌گیریم
    return extracted_text, result  # برگرداندن نتیجه به همراه مختصات


# 2. تابع برای اصلاح املای متن با SpellChecker
def correct_spelling(text):
    spell = SpellChecker()
    corrected_text = []
    for word in text.split():
        # پیدا کردن غلط املایی و اصلاح آن
        corrected_word = spell.correction(word)
        if corrected_word is None:  # اگر اصلاح نشد، کلمه اصلی رو برمی‌گردونیم
            corrected_word = word
        corrected_text.append(corrected_word)
    return " ".join(corrected_text)


# 3. تابع برای رسم متن اصلاح‌شده روی تصویر
def draw_text_on_image(image, extracted_text, result):
    for (bbox, text_detected, prob) in result:
        # گرفتن مختصات اولین گوشه برای رسم متن
        pt1 = (int(bbox[2][0]), int(bbox[0][1]))  # استفاده از اولین نقطه در bbox به عنوان (x, y)

        # رسم متن شناسایی‌شده روی تصویر
        cv2.putText(image, text_detected, pt1, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    return image


# 4. تابع اصلی که تصویر را پردازش می‌کند
# 4. تابع اصلی که تصویر را پردازش می‌کند
def main(image_path, output_path="output_image.png"):
    image = cv2.imread(image_path)

    # استخراج متن از تصویر
    extracted_text, result = extract_text_with_easyocr(image)
    print("Extracted Text:", extracted_text)

    # اصلاح املای متن استخراج‌شده
    for text in extracted_text:
        corrected_text = correct_spelling(text)
        print("Corrected Text:", corrected_text)

    # رسم متن اصلاح‌شده روی تصویر
    final_image_with_text = draw_text_on_image(image.copy(), corrected_text, result)

    # ذخیره کردن تصویر نهایی
    cv2.imwrite(output_path, final_image_with_text)
    print(f"Processed image saved as {output_path}")

    # نمایش تصویر نهایی با متن اصلاح‌شده
    cv2.imshow("Processed Image with Text", final_image_with_text)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# اجرای برنامه با مسیر تصویر مورد نظر و مسیر ذخیره‌سازی
image_path = "sample_image.png"
output_path = "corrected_output_image.png"
main(image_path, output_path)

