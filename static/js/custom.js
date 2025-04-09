
function searchRecipes() {
    var input, filter, recipeList, cards, card, title, i, txtValue;
    input = document.getElementById("recipeSearch");
    filter = input.value.toLowerCase();
    recipeList = document.getElementById("recipeList");
    cards = recipeList.getElementsByClassName("recipe-card");

    // Loop through all recipe cards and hide those that don't match the search query
    for (i = 0; i < cards.length; i++) {
        card = cards[i];
        title = card.getElementsByClassName("card-title")[0];
        txtValue = title.textContent || title.innerText;
        if (txtValue.toLowerCase().indexOf(filter) > -1) {
            card.style.display = "";
        } else {
            card.style.display = "none";
        }
    }
}