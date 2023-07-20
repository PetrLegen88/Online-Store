
const currentUrl = window.location.href;
if (currentUrl === 'http://127.0.0.1:8000/') {

const form = document.getElementById('price-form');
const categoryInput = document.getElementById('category');
const minPriceInput = document.getElementById('min-price');
const maxPriceInput = document.getElementById('max-price');
const resultsContainer = document.getElementById('results-container');

const buildUrl = () => {
  let url = 'http://127.0.0.1:8000/'; // start with the base URL
  const category = categoryInput.value;
  const minPrice = minPriceInput.value;
  const maxPrice = maxPriceInput.value;
  if (category && minPrice && maxPrice) {
    url += `categories/${category}/price/range/${minPrice}/${maxPrice}/`;
  } else if (category && minPrice) {
    url += `categories/${category}/price/min/${minPrice}/`;
  } else if (category && maxPrice) {
    url += `categories/${category}/price/max/${maxPrice}/`;
  } else if (minPrice && maxPrice) {
    url += `price/range/${minPrice}/${maxPrice}/`;
  } else if (minPrice) {
    url += `price/min/${minPrice}/`;
  } else if (maxPrice) {
    url += `price/max/${maxPrice}/`;
  } else if (category) {
    url += `categories/${category}/`;
  }
  return url;
};

const submitForm = async () => {
  const url = buildUrl();
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.text();
    resultsContainer.innerHTML = data;
  } catch (error) {
    console.error(error);
  }
};

// Submit the form when the user changes any of the search criteria
categoryInput.addEventListener('change', submitForm);
minPriceInput.addEventListener('change', submitForm);
maxPriceInput.addEventListener('change', submitForm);

// Submit the form initially to display the default results
submitForm();

// Prevent the form from reloading the page on submit
form.addEventListener('submit', (event) => {
  event.preventDefault();
  submitForm();
});
}
