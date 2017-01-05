var Train = Backbone.Model.extend({
    idAttribute: 'train_name',

    url: function() {
        return 'api/trains/' + this.get('train_name');
    },

    matchFilter: function(filter) {
        filter = filter.toLowerCase();
        return this.get("train_name").toLowerCase().indexOf(filter) >= 0 ||
            _.some(this.get("stations"), function(s) {
                return s.toLowerCase().indexOf(filter) >= 0
            });
    }
});

var Trains = Backbone.Collection.extend({
    model: Train,
    url: 'api/trains',

    parse: function(resp) {
        return resp.trains;
    }
});

var MainView = Backbone.View.extend({
    el: '#page',
    template: _.template($('#main-template').html()),
    filterTimeout: 300,
    nameFilter: '',
    lastFilterValue: '',

    events: {
        'keyup': function(e) {
            if (e.target.value != this.nameFilter) {
                var that = this;
                this.nameFilter = e.target.value;
                clearTimeout(this.timer);
                this.timer = setTimeout(function() {
                    that.render();
                }, this.filterTimeout);
            }
        }
    },

    activate: function() {
        if (!this.trains) {
            var that = this;
            this.trains = new Trains();
            this.trains.fetch({success: function() { that.render(); }});
        }
        this.render();
    },

    render: function() {
        var trains = this.trains;
        if (this.nameFilter) {
            var that = this
            trains = new Trains(trains.filter(function (train) {
                return train.matchFilter(that.nameFilter);
            }));

            this.$el.html(this.template({trains: trains.toJSON()}));

            $('#filter').focus();
            $('#filter').val(this.nameFilter);
        } else if (trains.length > 0) {
            this.$el.html(this.template({trains: trains.toJSON()}));
        } else {
            this.$el.html(this.template({trains: 'waiting'}));
        }

        document.title = 'InfoPasażer Archiver - archiwum opóźnień pociągów';
        return this;
    }
});

var TrainView = Backbone.View.extend({
    el: '#page',
    template: _.template($('#train-template').html()),

    activate: function(name) {
        var that = this;
        var train = new Train({train_name: name});
        train.fetch({success: function(train) { that.render(train); }});
    },

    render: function(train) {
        this.$el.html(this.template(train.toJSON()));
        document.title = train.get('train_name');
        return this;
    }
});

var Router = Backbone.Router.extend({
    routes: {
        '': 'index',
        'train/*name': 'train'
    },

    initialize: function() {
        this.mainView = new MainView();
        this.trainView = new TrainView();
    },

    index: function() {
        this.mainView.activate();
    },

    train: function(name) {
        this.trainView.activate(name);
    }
});

var router = new Router();
Backbone.history.start();
