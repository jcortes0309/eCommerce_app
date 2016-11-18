var app = angular.module("e-commerce", ["ui.router"]);










// States
app.config(function($stateProvider, $urlRouterProvider) {
  $stateProvider
    .state({
      name: "products",
      url: "/products",
      templateUrl: "products.html",
      controller: "ProductsController"
    })
    .state({
      name: "product_details",
      url: "/product_details/{productId}",
      templateUrl: "product_details.html",
      controller: "DetailsController"
    })
    .state({
      name: "signup",
      url: "/signup",
      templateUrl: "signup.html",
      controller: "SignUpController"
    })
    .state({
      name: "login",
      url: "/login",
      templateUrl: "login.html",
      controller: "LoginController"
    })
    .state({
      name: "shopping_cart",
      url: "/shopping_cart/{customerId}",
      templateUrl: "shopping_cart.html",
      controller: "ShoppingCartController"
    });
});
