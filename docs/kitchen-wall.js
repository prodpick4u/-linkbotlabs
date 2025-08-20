document.addEventListener("DOMContentLoaded", () => {
  const wall = document.getElementById("kitchen-wall");

  const products = [
    {
      name: "Air Fryer",
      url: "https://www.amazon.com/s?k=air+fryer&tag=mychanneld-20",
      img: "https://m.media-amazon.com/images/I/71Q0A0W7dCL._AC_SX679_.jpg"
    },
    {
      name: "Rice Cooker",
      url: "https://www.amazon.com/s?k=rice+cooker&tag=mychanneld-20",
      img: "https://m.media-amazon.com/images/I/71ssYyQdSxL._AC_SX679_.jpg"
    },
    {
      name: "Blender",
      url: "https://www.amazon.com/s?k=blender&tag=mychanneld-20",
      img: "https://m.media-amazon.com/images/I/71Bf+cj1L8L._AC_SX679_.jpg"
    },
    {
      name: "Coffee Maker",
      url: "https://www.amazon.com/s?k=coffee+maker&tag=mychanneld-20",
      img: "https://m.media-amazon.com/images/I/71Z5FqD+f3L._AC_SX679_.jpg"
    },
    {
      name: "Knife Set",
      url: "https://www.amazon.com/s?k=kitchen+knife+set&tag=mychanneld-20",
      img: "https://m.media-amazon.com/images/I/81U+qv9qUuL._AC_SX679_.jpg"
    },
    {
      name: "Cookware Set",
      url: "https://www.amazon.com/s?k=cookware+set&tag=mychanneld-20",
      img: "https://m.media-amazon.com/images/I/81t7YxG6PCL._AC_SX679_.jpg"
    }
  ];

  products.forEach(p => {
    const item = document.createElement("a");
    item.href = p.url;
    item.target = "_blank";
    item.className = "kitchen-item";
    item.innerHTML = `
      <img src="${p.img}" alt="${p.name}">
      <p>${p.name}</p>
    `;
    wall.appendChild(item);
  });
});
