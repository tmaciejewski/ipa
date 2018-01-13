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
    },

    parse: function(train) {
        if (train.stations) {
            train.activeStation = 1;
            train.firstIntermediateStation = 1;
            train.lastIntermediateStation = train.stations.length - 2;
        }
        return train;
    },

    nextStation: function() {
        var activeStation = this.get("activeStation");
        this.set("activeStation", activeStation + 1);
    },

    prevStation: function() {
        var activeStation = this.get("activeStation");
        this.set("activeStation", activeStation - 1);
    }
});

var Trains = Backbone.Collection.extend({
    model: Train,
    url: 'api/trains',

    parse: function(resp) {
        return resp.trains;
    }
});

var MainItemView = Backbone.View.extend({
    tagName: 'tr',
    template: _.template($('#main-item-template').html()),

    events: {
        'click .prev-station': 'prevStation',
        'click .next-station': 'nextStation'
    },

    initialize: function() {
        this.listenTo(this.model, 'change', this.render);
    },

    prevStation: function() {
        this.model.prevStation();
    },

    nextStation: function() {
        this.model.nextStation();
    },

    render: function() {
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    }
});

var MainView = Backbone.View.extend({
    el: '#page',
    template: _.template($('#main-template').html()),
    filterTimeout: 200,
    nameFilter: '',
    nameFilterMin: 2,
    lastFilterValue: '',
    page: 0,
    trainsPerPage: 100,

    events: {
        'click .next-page': 'nextPage',
        'click .prev-page': 'prevPage',
        'keyup #filter': 'filterChanged'
    },

    activate: function() {
        if (!this.allTrains) {
            var that = this;
            this.allTrains = new Trains();
            this.allTrains.fetch({
                success: function() { that.state = 'ok'; that.render(); },
                error: function() { that.state = 'error'; that.render(); }
            });
            this.state = 'waiting';
        }
        document.title = 'InfoPasażer Archiver - archiwum opóźnień pociągów';
        this.render();
    },

    nextPage: function() {
        this.page++;
        this.renderTrains();
    },

    prevPage: function() {
        this.page--;
        this.renderTrains();
    },

    filterChanged: function(e) {
        if (e.target.value != this.nameFilter) {
            var that = this;
            this.nameFilter = e.target.value;
            clearTimeout(this.timer);
            this.timer = setTimeout(function() {
                that.page = 0;
                that.renderTrains();
            }, this.filterTimeout);
        }
    },

    renderTrains: function() {
        var that = this;
        var trainListTemplate = _.template($('#main-table-template').html());
        var trains = [];
        var pageCount = 0;

        if (this.nameFilter != '') {
            trains = this.allTrains.filter(function (train) {
                return train.matchFilter(that.nameFilter);
            });
        } else {
            trains = this.allTrains.toArray();
        }

        if (trains.length > 0) {
            pageCount = Math.ceil(trains.length / this.trainsPerPage);
            trains = _.first(_.rest(trains, this.page * this.trainsPerPage), this.trainsPerPage);
        }

        $('#main-content').html(trainListTemplate({state: this.state, page: this.page + 1, pageCount: pageCount, size: trains.length}));

        _.each(trains, function(train) {
            var view = new MainItemView({model: train});
            $('#main-table').append(view.render().el);
        });
    },

    render: function() {
        this.$el.html(this.template());
        this.renderTrains();
        return this;
    }
});

var TrainView = Backbone.View.extend({
    el: '#page',

    activate: function(name) {
        var that = this;
        var train = new Train({train_name: name});
        train.fetch({
            success: function(train) { that.render(train); },
            error: function() { that.error(); }
        });
        document.title = name;
    },

    render: function(train) {
        var template = _.template($('#train-template').html());
        this.$el.html(template(train.toJSON()));
        return this;
    },

    error: function() {
        var template = _.template($('#error-template').html());
        this.$el.html(template({msg: 'Nie ma takiego pociągu'}));
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
