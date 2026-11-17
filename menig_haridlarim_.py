import sqlite3

DB_NOMI = "menig_haridlarim.db"


def bazaga_ulanish():
    conn = sqlite3.connect(DB_NOMI)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            bajarildi INTEGER NOT NULL DEFAULT 0
        )
        """
    )
    conn.commit()
    return conn


def id_kiritish():
    matn = input("Harid ID raqamini kiriting: ").strip()
    if not matn.isdigit():
        print("Xato: ID raqam bo'lishi kerak.")
        return None
    return int(matn)


def haridni_chiqarish(qator):
    holat = "olingan" if qator[2] else "olinmagan"
    print(f"ID: {qator[0]} | {qator[1]} | {holat}")


def mahsulot_qoshish(conn):
    nom = input("Mahsulot nomini kiriting: ").strip()
    if not nom:
        print("Xato: nom bo'sh bo'lmasligi kerak.")
        return
    conn.execute("INSERT INTO tasks (nom) VALUES (?)", (nom,))
    conn.commit()
    print("Harid qo'shildi.")


def barcha_haridlar(conn):
    qatorlar = conn.execute("SELECT id, nom, bajarildi FROM tasks ORDER BY id").fetchall()
    if not qatorlar:
        print("Haridlar mavjud emas.")
        return
    for qator in qatorlar:
        haridni_chiqarish(qator)


def haridni_qidirish(conn):
    task_id = id_kiritish()
    if task_id is None:
        return
    qator = conn.execute(
        "SELECT id, nom, bajarildi FROM tasks WHERE id = ?", (task_id,)
    ).fetchone()
    if qator:
        haridni_chiqarish(qator)
    else:
        print("Xato: bunday ID li harid topilmadi.")


def haridlarni_yangilash(conn):
    task_id = id_kiritish()
    if task_id is None:
        return
    yangi_nom = input("Yangi harid nomini kiriting: ").strip()
    if not yangi_nom:
        print("Xato: nom bo'sh bo'lmasligi kerak.")
        return
    cur = conn.execute("UPDATE tasks SET nom = ? WHERE id = ?", (yangi_nom, task_id))
    conn.commit()
    if cur.rowcount:
        print("Harid nomi yangilandi.")
    else:
        print("Bunday ID li harid topilmadi.")


def qabul_qilingan_haridlar(conn):
    qatorlar = conn.execute(
        "SELECT id, nom, bajarildi FROM tasks WHERE bajarildi = 1 ORDER BY id"
    ).fetchall()
    if not qatorlar:
        print("Qabul qilingan haridlar yo'q.")
        return
    for qator in qatorlar:
        haridni_chiqarish(qator)


def haridni_ochirish(conn):
    task_id = id_kiritish()
    if task_id is None:
        return
    cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    if cur.rowcount:
        print("Harid o'chirildi.")
    else:
        print("Bunday ID li harid topilmadi.")


def haridni_belgilash(conn):
    task_id = id_kiritish()
    if task_id is None:
        return
    cur = conn.execute("UPDATE tasks SET bajarildi = 1 WHERE id = ?", (task_id,))
    conn.commit()
    if cur.rowcount:
        print("Harid olingan deb belgilandi.")
    else:
        print("Bunday ID li harid topilmadi.")


def menyu():
    print("\n=== Harid menejeri ===")
    print("1. Harid qo'shish")
    print("2. Barcha haridlar")
    print("3. Haridni (ID bo'yicha) qidirish")
    print("4. Haridni yangilash")
    print("5. Qabul qilingan haridlar")
    print("6. Haridni o'chirish")
    print("7. Haridni olingan deb belgilash")
    print("8. Chiqish")


def main():
    conn = bazaga_ulanish()
    amallar = {
        "1": mahsulot_qoshish,
        "2": barcha_haridlar,
        "3": haridni_qidirish,
        "4": haridlarni_yangilash,
        "5": qabul_qilingan_haridlar,
        "6": haridni_ochirish,
        "7": haridni_belgilash,
    }
    while True:
        menyu()
        tanlov = input("Tanlang (1-8): ").strip()
        if tanlov == "8":
            print("etiboringiz uchun rahmat hayr salomat boling")
            break
        amal = amallar.get(tanlov)
        if amal:
            amal(conn)
        else:
            print("Xato: 1 dan 8 gacha raqam kiriting.")
    conn.close()


if __name__ == "__main__":
    main()