
const menuData = {
    'snacks-appetizers': [
        { name: "Chicharon Bulaklak", description: "Crispy pork intestines", price: "₱250" },
        { name: "Crispy Veggie Okoy", description: "Vegetable fritters", price: "₱200" },
        { name: "Crispy Veggie Okoy Jr.", description: "Small veggie fritters", price: "₱140" },
        { name: "Batangas Pupod", description: "Local delicacy", price: "₱275" },
        { name: "Chicken Fillet", description: "Breaded chicken strips", price: "₱225" },
        { name: "Fish Fillet Fingers", description: "Fried fish fillets", price: "₱225" },
        { name: "Quirky Nachos", description: "Nachos with a twist", price: "₱320" },
        { name: "Tokwa't Pupod", description: "Fried tofu with pork", price: "₱200" },
        { name: "Shrimp Tempura 6pcs", description: "Crispy shrimp tempura", price: "₱375" },
        { name: "Shrimp Tempura 12 pcs", description: "Dozen crispy shrimp tempura", price: "₱675" },
        { name: "Calamari", description: "Fried squid rings", price: "₱250" },
        { name: "Gambas al Ajillo", description: "Shrimp in garlic sauce", price: "₱340" },
        { name: "Crispy SeaPod Platter", description: "Assorted fried seafood", price: "₱525" },
        { name: "Crispy ChickBoy Platter", description: "Assorted fried chicken parts", price: "₱475" },
        { name: "Pansit Bihon", description: "Stir-fried rice noodles", price: "₱275" },
        { name: "Pansit Bihon Canton", description: "Mixed rice and egg noodles", price: "₱315" },
        { name: "Pansit Canton Guisado", description: "Stir-fried egg noodles", price: "₱275" },
        { name: "Crispy Canton", description: "Crispy egg noodles", price: "₱300" },
        { name: "Miki Bihon", description: "Mixed stir-fried noodles", price: "₱275" }
    ],
    'breakfast-meals': [
        { name: "Daing na Bangus", description: "Fried marinated milkfish", price: "₱340" },
        { name: "Pork Tocino", description: "Sweet cured pork", price: "₱325" },
        { name: "Pork Tapang Taal", description: "Marinated pork tapa", price: "₱340" },
        { name: "Beef Tapa", description: "Marinated beef strips", price: "₱360" },
        { name: "Longganisang Taal", description: "Local sausage", price: "₱275" },
        { name: "Beef Pares", description: "Beef stew with garlic rice", price: "₱365" },
        { name: "Sinaing na Tulingan", description: "Stewed bullet tuna", price: "₱340" },
        { name: "Chicken Longganisa", description: "Chicken sausage", price: "₱275" },
        { name: "Italian Garlic Sausage", description: "Spicy Italian sausage", price: "₱325" },
        { name: "Schublig Sausage", description: "Swiss sausage", price: "₱365" },
        { name: "Barako Breakfast", description: "Traditional breakfast platter", price: "₱400" },
        { name: "Wonton Mami", description: "Noodle soup with wontons", price: "₱275" },
        { name: "Beef Mami", description: "Noodle soup with beef", price: "₱300" },
        { name: "Beef Wonton Mami", description: "Noodle soup with beef and wontons", price: "₱325" },
        { name: "Regular Lomi", description: "Egg noodle soup", price: "₱275" },
        { name: "Jumbo Lomi", description: "Large egg noodle soup", price: "₱340" },
        { name: "Super Jumbo Lomi", description: "Extra large egg noodle soup", price: "₱425" },
        { name: "Plain Rice", description: "Steamed white rice", price: "₱85" },
        { name: "Garlic Rice", description: "Steamed rice with garlic", price: "₱110" },
        { name: "Plain Rice Platter", description: "Large portion of plain rice", price: "₱225" },
        { name: "Garlic Rice Platter", description: "Large portion of garlic rice", price: "₱275" },
        { name: "Karibok Rice Platter", description: "Specialty rice platter", price: "₱330" },
        { name: "Chicken Binakol", description: "Chicken soup with coconut", price: "₱375" },
        { name: "Batangas Bulalo", description: "Beef marrow soup", price: "₱425" },
        { name: "Sinigang na Salmon", description: "Salmon in sour soup", price: "₱365" },
        { name: "Sinigang na Pork Belly", description: "Pork belly in sour soup", price: "₱340" },
        { name: "Sinigang na Hipon", description: "Shrimp in sour soup", price: "₱375" },
        { name: "Pinakbet", description: "Stewed mixed vegetables", price: "₱275" },
        { name: "Laing", description: "Taro leaves in coconut milk", price: "₱250" },
        { name: "Chop Suey", description: "Stir-fried mixed vegetables", price: "₱325" },
        { name: "Beef Ampalaya", description: "Beef with bitter melon", price: "₱340" },
        { name: "Beef Broccoli", description: "Beef with broccoli", price: "₱340" },
        { name: "Sizzling Pork Sisig", description: "Sizzling chopped pork", price: "₱325" },
        { name: "Sizzling Bulalo", description: "Sizzling beef shank", price: "₱375" },
        { name: "Sizzling Tofu Pupod", description: "Sizzling tofu with pork", price: "₱330" },
        { name: "Sizzling Tuna & Shrimp", description: "Sizzling tuna and shrimp", price: "₱375" },
        { name: "Tuna Belly", description: "Grilled tuna belly", price: "₱385" },
        { name: "Tuna Belly with Teriyaki Sauce", description: "Tuna belly in teriyaki sauce", price: "₱415" },
        { name: "Inihaw na Liempo", description: "Grilled pork belly", price: "₱325" },
        { name: "Chicken Barbecue", description: "Grilled marinated chicken", price: "₱340" },
        { name: "Crispy Pata", description: "Crispy pork knuckles", price: "₱475" },
        { name: "Lechon Kawali", description: "Crispy pork belly", price: "₱425" },
        { name: "Cordon Bleu", description: "Breaded chicken stuffed with ham and cheese", price: "₱385" },
        { name: "Whole Fried Chicken", description: "Fried whole chicken", price: "₱675" },
        { name: "Fried Tawilis", description: "Fried freshwater sardines", price: "₱325" },
        { name: "Chicken Kare-kare", description: "Chicken in peanut sauce", price: "₱365" },
        { name: "Beef Kare-kare", description: "Beef in peanut sauce", price: "₱400" },
        { name: "Pork Kaldereta", description: "Pork stew in tomato sauce", price: "₱365" },
        { name: "Pork Pochero", description: "Pork stew with vegetables", price: "₱375" },
        { name: "Lengua Estofado", description: "Ox tongue in tomato sauce", price: "₱425" },
        { name: "Pechay Rolls", description: "Stuffed pechay rolls", price: "₱340" },
        { name: "Sinaing na Tulingan", description: "Stewed bullet tuna", price: "₱340" },
        { name: "Salmon Steak", description: "Grilled salmon steak", price: "₱425" },
        { name: "Ribeye Steak", description: "Grilled ribeye steak", price: "₱675" },
        { name: "Sizzling Pork Tenderloin", description: "Sizzling pork tenderloin", price: "₱425" },
        { name: "Sizzling Chicken Steak", description: "Sizzling chicken steak", price: "₱375" }
    ],
    'desserts-beverages': [
        { name: "Suman Alitagtag piece", description: "Sticky rice cake", price: "₱120",},
        { name: "Suman Pack of 12", description: "Dozen sticky rice cakes", price: "₱200" },
        { name: "3 pieces Suman at Kapeng Barako", description: "Sticky rice cake with coffee", price: "₱230"},
        { name: "Unli Barako Upgrade", description: "Unlimited local coffee", price: "₱350"},
        { name: "Special Halo-Halo", description: "Mixed dessert with shaved ice", price: "₱175"},
        { name: "Barakoffee Jelly", description: "Coffee-flavored jelly", price:"₱150"}
    ]

};

function showMenu(section) {
    const menuSection = document.getElementById('menu-section');
    const showcase = document.getElementById('showcase');
    const menuTitle = document.getElementById('menu-title');
    const menuItems = document.getElementById('menu-items');

    menuSection.style.display = 'block';
    showcase.style.display = 'none';

    menuTitle.textContent = section.replace('-', ' & ').toUpperCase();
    menuItems.innerHTML = '';

    menuData[section].forEach(item => {
        menuItems.innerHTML += `
            <div class="menu-item">
                <h4>${item.name}</h4>
                <p>${item.description}</p>
                <span class="price">${item.price}</span>
            </div>
        `;
    });
}

function goBack() {
    document.getElementById('menu-section').style.display = 'none';
    document.getElementById('showcase').style.display = 'block';
}

// Load the last section from sessionStorage if available
window.onload = function() {
    const lastMenuSection = sessionStorage.getItem('lastMenuSection');
    if (lastMenuSection) {
        showMenu(lastMenuSection);
    }
};