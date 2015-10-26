app.factory('TwitterFactory',['$http', function ( $http ) {

  var authTweets = function ( sessionToken ) {
    return $http({
      method: 'GET',
      url: '/activate',
      params: { sessionToken : sessionToken }
    });
  };

  var getTweets = function ( ) {
    return $http({
      method: 'GET',
      url: '/tweetsfeed'
    });
  };

  var favTweet = function ( id ) {
    return $http({
      method: 'POST',
      url: '/favtweet',
      data: { id: id }
    });
  };

  var reTweet = function ( id ) {
    return $http({
      method: 'POST',
      url: '/retweet',
      data: { id: id }
    });
  };

  return {
    authTweets: authTweets,
    getTweets: getTweets,
    favTweet: favTweet,
    reTweet: reTweet
  };

}])
  .filter('tweetLinky',['$filter', function($filter) {
    return function(text, target) {
      if (!text) return text;

      var replacedText = $filter('linky')(text, target);
      var targetAttr = "";
      if (angular.isDefined(target)) {
          targetAttr = ' target="' + target + '"';
      }
      // replace #hashtags and send them to twitter
      var replacePattern1 = /(^|\s)#(\w*[a-zA-Z_]+\w*)/gim;
      replacedText = text.replace(replacePattern1, '$1<a href="https://twitter.com/search?q=%23$2"' + targetAttr + '>#$2</a>');
      // replace @mentions but keep them to our site
      var replacePattern2 = /(^|\s)\@(\w*[a-zA-Z_]+\w*)/gim;
      replacedText = replacedText.replace(replacePattern2, '$1<a href="https://twitter.com/$2"' + targetAttr + '>@$2</a>');
      return replacedText;
    };
  }
]);