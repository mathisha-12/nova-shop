import sqlite3
DB = "shop.db"

PRODUCTS = [
    ("Aurora Wireless Headphones", 189, "Electronics", "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80", "Immersive sound with ANC and 40-hour battery.", 4.8),
    ("Cloudstep Sneakers", 129, "Fashion", "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&q=80", "Lightweight sneakers with breathable mesh upper.", 4.6),
    ("Meridian Chrono Watch", 249, "Accessories", "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=80", "Stainless steel chronograph with sapphire crystal.", 4.9),
    ("Eclipse Sunglasses", 79, "Accessories", "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=800&q=80", "Polarized UV400 lenses with acetate frame.", 4.5),
    ("Nimbus Smart Speaker", 149, "Electronics", "https://images.unsplash.com/photo-1543512214-318c7553f230?w=800&q=80", "Room-filling 360° sound with voice assistant.", 4.4),
    ("Linen Oversized Shirt", 69, "Fashion", "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=800&q=80", "Breathable European linen, relaxed silhouette.", 4.3),
    ("Terra Ceramic Mug Set", 39, "Home", "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=800&q=80", "Handcrafted stoneware mugs, set of four.", 4.7),
    ("Atlas Leather Backpack", 199, "Accessories", "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&q=80", "Full-grain leather, fits a 15\" laptop.", 4.8),
    ("Lumen Desk Lamp", 89, "Home", "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800&q=80", "Warm dimmable LED with a sculptural brass arm.", 4.6),
    ("Vista Mechanical Keyboard", 159, "Electronics", "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&q=80", "Hot-swappable switches with PBT keycaps.", 4.7),
    ("Drift Yoga Mat", 59, "Fitness", "https://images.unsplash.com/photo-1592432678016-e910b452f9a2?w=800&q=80", "Non-slip cork surface with rubber base.", 4.5),
    ("Kindle Wool Throw", 119, "Home", "https://images.unsplash.com/photo-1600166898405-da9535204843?w=800&q=80", "Pure merino wool throw, woven in Portugal.", 4.9),
]

con = sqlite3.connect(DB); cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS products")
cur.execute("""CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT, price REAL, category TEXT,
    image TEXT, description TEXT, rating REAL)""")
cur.executemany("INSERT INTO products (name,price,category,image,description,rating) VALUES (?,?,?,?,?,?)", PRODUCTS)
con.commit(); con.close()
print(f"Seeded {len(PRODUCTS)} products into {DB}")
