#คำอธิบายภาพรวมของ Module ว่าเป็นไฟล์รวมฟังก์ชันวัดผลโมเดล (F1-score, ROC-AUC, RMSE)
"""
Custom metrics utilities for model evaluation.

Supported metrics:
- F1-score
- ROC-AUC
- RMSE
"""
#ดึง Optional จาก Module typing มาใช้ระบุว่าตัวแปรนั้นๆ สามารถเป็น None หรือชนิดข้อมูลตามที่กำหนดได้
from typing import Optional

#ดึง Library numpy เข้ามาใช้งาน และตั้งชื่อย่อว่า np สำหรับจัดการข้อมูลประเภท Array
import numpy as np
#ดึงฟังก์ชันคำนวณ Metric มาตรฐาน (f1_score, mean_squared_error, roc_auc_score) มาจาก scikit-learn
from sklearn.metrics import f1_score, mean_squared_error, roc_auc_score

#ฟังก์ชัน calculate_f1
def calculate_f1(
    #ประกาศฟังก์ชันสำหรับคำนวณค่า F1-Score
    #พารามิเตอร์รับ Array ของ คำตอบที่ถูกต้อง (Ground Truth)
    y_true: np.ndarray,
    #พารามิเตอร์รับ Array ของ ค่าที่โมเดลทำนาย ออกมา
    y_pred: np.ndarray,
    #พารามิเตอร์กำหนดรูปแบบการเฉลี่ยผล (Default คือ "binary" สำหรับจำแนก 2 คลาส)
    average: str = "binary",
) -> float:
#กำหนดให้ฟังก์ชันนี้ คืนค่าผลลัพธ์กลับมาเป็นทศนิยม (float)
    #อธิบายรายละเอียดการใช้งานฟังก์ชัน
    """
    Calculate F1-score.

    Args:
        y_true: Ground-truth labels.
        y_pred: Predicted labels.
        average: Averaging strategy.
            - "binary" for binary classification
            - "macro" for multiclass classification
            - "weighted" for weighted multiclass classification

    Returns:
        F1-score as a float.
    """
    #เรียกใช้ f1_score จาก sklearn โดยใส่ zero_division=0 เพื่อป้องกัน Error กรณีมีการหารด้วยศูนย์ แล้วแปลงผลลัพธ์เป็น float ก่อนส่งกลับ
    return float(f1_score(y_true, y_pred, average=average, zero_division=0))

#ฟังก์ชัน calculate_roc_auc
def calculate_roc_auc(
    #ประกาศฟังก์ชันสำหรับคำนวณค่า ROC-AUC Score
    #รับ Array ของคำตอบที่ถูกต้อง
    y_true: np.ndarray,
    #รับ Array ของค่าความน่าจะเป็น (Probability) ที่โมเดลทำนายได้
    y_score: np.ndarray,
    #รับการตั้งค่ารูปแบบ Multiclass ("ovr", "ovo") หรือเป็น None ถ้าเป็น Binary Classification
    multi_class: Optional[str] = None,
) -> float:
#ส่งคืนผลลัพธ์เป็น float
    #ตรวจสอบว่า ถ้าไม่ได้ระบุรูปแบบ Multiclass (กรณีเป็น Binary Classification)
    """
    Calculate ROC-AUC.

    Args:
        y_true: Ground-truth labels.
        y_score: Predicted probability or decision score.
        multi_class:
            - None for binary classification
            - "ovr" or "ovo" for multiclass classification

    Returns:
        ROC-AUC score as a float.
    """
    #ตรวจสอบว่า ถ้าไม่ได้ระบุรูปแบบ Multiclass (กรณีเป็น Binary Classification)
    if multi_class is None:
        #คำนวณ ROC-AUC แบบปกติ แปลงเป็น float แล้วส่งกลับทันที
        return float(roc_auc_score(y_true, y_score))
    #ถ้าเงื่อนไขข้างต้นไม่เป็นจริง (เป็น Multiclass) ให้เตรียมส่งคืนค่าทศนิยมที่ได้จากบรรทัดถัดไป
    return float(
        #เรียกใช้ฟังก์ชันคำนวณ ROC-AUC ของ sklearn
        roc_auc_score(
            #ส่งค่าคำตอบที่ถูกต้องเข้าไป
            y_true,
            #ส่งค่าความน่าจะเป็นของแต่ละคลาสเข้าไป
            y_score,
            #ส่งกลยุทธ์การคำนวณสำหรับ Multiclass ("ovr" หรือ "ovo") เข้าไป
            multi_class=multi_class,
        )
    )

#ฟังก์ชัน calculate_rmse
def calculate_rmse(
    #ประกาศฟังก์ชันคำนวณค่า Root Mean Squared Error สำหรับโจทย์ Regression
    #รับ Array ของค่าจริงที่เป็นตัวเลขต่อเนื่อง
    y_true: np.ndarray,
    #รับ Array ของค่าตัวเลขที่โมเดลทำนายได้
    y_pred: np.ndarray,
) -> float:
#ส่งคืนผลลัพธ์เป็น float
    """
    Calculate Root Mean Squared Error (RMSE).

    Args:
        y_true: Ground-truth continuous values.
        y_pred: Predicted continuous values.

    Returns:
        RMSE as a float.
    """
    #เตรียมแปลงผลลัพธ์การคำนวณเป็น float เพื่อส่งกลับ
    return float(
        #ใช้ NumPy ถอดรากที่สอง (Square Root) จากค่า MSE ที่คำนวณได้
        np.sqrt(
            #คำนวณค่า Mean Squared Error (ความต่างยกกำลังสองเฉลี่ย) ระหว่างค่าจริงกับค่าทำนาย
            mean_squared_error(y_true, y_pred)
        )
    )

#ฟังก์ชัน calculate_classification_metrics
def calculate_classification_metrics(
    #ประกาศฟังก์ชันตัวรวบสำหรับคำนวณ Metric ฝั่ง Classification ทั้งหมดในครั้งเดียว
    #รับ Array ของคำตอบที่ถูกต้อง
    y_true: np.ndarray,
    #รับ Array ของค่าคลาสที่ทำนายได้
    y_pred: np.ndarray,
    #รับ Array ของความน่าจะเป็น (ใส่หรือไม่ใส่ก็ได้ Default คือ None)
    y_score: Optional[np.ndarray] = None,
    #กำหนดการเฉลี่ย F1-score (Default คือ "binary")
    average: str = "binary",
    #กำหนดกลยุทธ์ Multiclass สำหรับ ROC-AUC (Default คือ None)
    multi_class: Optional[str] = None,
) -> dict[str, float]:
#กำหนดให้ส่งคืนผลลัพธ์ออกมาเป็น Dictionary ที่มี Key เป็นข้อความ และ Value เป็นตัวเลขทศนิยม
    #สร้าง Dictionary ชื่อ metrics ขึ้นมารองรับผลลัพธ์
    metrics = {
        #คำนวณ F1-Score แล้วเก็บไว้ใน Key "f1"
        "f1": calculate_f1(
            #ส่ง Array คำตอบจริงเข้าฟังก์ชัน calculate_f1
            y_true,
            #ส่ง Array ค่าทำนายเข้าฟังก์ชัน calculate_f1
            y_pred,
            #ส่งรูปแบบการเฉลี่ยเข้าฟังก์ชัน calculate_f1
            average=average,
        )
    }
    #ตรวจสอบว่า มีการส่งค่าความน่าจะเป็น (y_score)เข้ามาหรือไม่
    if y_score is not None:
        #ถ้าส่งมา ให้คำนวณ ROC-AUC แล้วเพิ่ม Key "roc_auc" เข้าไปใน Dictionary
        metrics["roc_auc"] = calculate_roc_auc(
            #ส่ง Array คำตอบจริงเข้าฟังก์ชัน calculate_roc_auc
            y_true,
            #ส่ง Array ค่าความน่าจะเป็นเข้าฟังก์ชัน calculate_roc_auc
            y_score,
            #ส่งรูปแบบ Multiclass เข้าฟังก์ชัน calculate_roc_auc
            multi_class=multi_class,
        )
    #ส่งคืน Dictionary รวมผลวัดผล Classification กลับไป
    return metrics

#ฟังก์ชัน calculate_regression_metrics
def calculate_regression_metrics(
    #ประกาศฟังก์ชันตัวรวบสำหรับคำนวณ Metric ฝั่ง Regression
    #รับ Array ของค่าจริง
    y_true: np.ndarray,
    #รับ Array ของค่าที่ทำนายได้
    y_pred: np.ndarray,
) -> dict[str, float]:
#กำหนดการส่งคืนค่าเป็น Dictionary
    """
    Calculate regression metrics.

    Returns:
        Dictionary containing RMSE.
    """
    #คืนค่า Dictionary ออกไปทันที
    return {
        #คำนวณค่า RMSE แล้วเก็บไว้ใต้ Key "rmse"
        "rmse": calculate_rmse(
            #ส่ง Array ค่าจริงเข้าฟังก์ชัน calculate_rmse
            y_true,
            #ส่ง Array ค่าทำนายเข้าฟังก์ชัน calculate_rmse
            y_pred,
        )
    }