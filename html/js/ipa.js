var Train = Backbone.Model.extend({
    defaults: {
        from: '',
        to: ''
    },

    matchFilter: function(filter) {
        filter = filter.toLowerCase();
        return this.get("id").toLowerCase().indexOf(filter) >= 0 ||
               this.get("from").toLowerCase().indexOf(filter) >= 0 ||
               this.get("to").toLowerCase().indexOf(filter) >= 0;
    }

});

var Trains = Backbone.Collection.extend({
    model: Train,

    url: 'api/trains'
});

var FilterView = Backbone.View.extend({
    el: '#filter',

    events: {
        'keyup': function() { this.trigger('changed', this.$el.val()); }
    }
});

var AppView = Backbone.View.extend({
    el: '#main',

    template: _.template($('#item-template').html()),

    trains: new Trains(),

    filterView: new FilterView(),

    initialize: function() {
        var that = this;
        this.trains.fetch({success: function() { that.render() }});
        this.filterView.on('changed', function(filter) { that.render(filter); });
    },

    render: function(filter) {
        var trains;
        if (filter) {
            trains = new Trains(this.trains.filter(function (train) {
                return train.matchFilter(filter);
            }));
        } else {
            trains = this.trains;
        }

        this.$el.html(this.template({trains: trains.toJSON()}));
        return this;
    }
});

var appView = new AppView();

