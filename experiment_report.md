# Experiment Report: Data Quality Impact on AI Agent

**Student ID:** AI20K-2004
**Name:** Dat Nguyen Tien
**Date:** 2026-04-15

---

## 1. Ket qua thi nghiem

Chay `agent_simulation.py` voi 2 bo du lieu va ghi lai ket qua:

| Scenario | Agent Response | Accuracy (1-10) | Notes |
|----------|----------------|-----------------|-------|
| Clean Data (`processed_data.csv`) | "the best choice is **Laptop** at $1200" | 9/10 | Correct — Laptop is the highest-priced legitimate electronic |
| Garbage Data (`garbage_data.csv`) | "the best choice is **Nuclear Reactor** at $999999" | 1/10 | Wrong — extreme outlier record ($999,999) hijacked the result |

---

## 2. Phan tich & nhan xet

### Tai sao Agent tra loi sai khi dung Garbage Data?

Khi chay voi `garbage_data.csv`, Agent da tra loi sai hoan toan vi bo du lieu bi "nhiem doc" boi nhieu van de chat luong nghiem trong:

**Duplicate IDs** lam mat tinh nhat quan cua du lieu. ID=1 xuat hien hai lan cho ca "Laptop" ($1200) va "Banana" ($2), vi vay bat ky logic nao phu thuoc vao ID duy nhat se co the cho ket qua khong xac dinh hoac sai lech.

**Outlier cuc doan** la van de nghiem trong nhat trong thu nghiem nay. Record "Nuclear Reactor" co gia $999,999 — mot gia tri phi thuc te, cao bat thuong so voi tat ca cac san pham con lai. Vi Agent su dung logic `idxmax()` de tim san pham co gia cao nhat trong danh muc "electronics", outlier nay da chiem quyen dieu khien ket qua va khien Agent de xuat mot san pham khong co that.

**Null values** trong cac truong `id` va `category` tao ra nhung hang "ma" (Ghost Items) ma Agent khong the xu ly hop ly. Neu logic phan loai dua vao category ma category la `None`, san pham se duoc bo qua hoac tao ra loi runtime.

**Sai kieu du lieu** (wrong data type) cho truong `price` voi gia tri la chuoi "ten dollars" thay vi so nguyen cung lam hong bat ky phep tinh so hoc nao, dan den loi hoac ket qua bat ngo.

Ket luan: mot Agent thong minh den dau cung chi co the hoat dong chinh xac khi du lieu no dua vao la sach va hop le. Du lieu rac phan anh thuc te ao — khong phan anh the gioi thuc — khien moi quyet dinh cua Agent tro nen vo nghia hoac nguy hiem.

---

## 3. Ket luan

**Quality Data > Quality Prompt?** — **Dong y hoan toan.**

Cho du prompt co duoc thiet ke tinh vi den dau, neu du lieu dau vao chua outlier, gia tri null, hoac ban ghi trung lap, Agent van se dua ra ket qua sai. Trong thu nghiem nay, chi voi mot record "Nuclear Reactor" gia tri $999,999, Agent da hoan toan mat kha nang phan biet dung san pham tot nhat cho nguoi dung. ETL pipeline voi validation nghiem ngat chinh la lop bao ve dau tien — va quan trong nhat — de dam bao chat luong cua bat ky he thong AI nao.
