$(function () {
    loadAll();
    $(".mode-btn").click(function () {
        var id = $(this).attr('id');
        var mode = Mode[id.substr(5)];
        setMode(mode);
        displayMode(mode);
    });
});
var Mode;
(function (Mode) {
    Mode["Off"] = "off";
    Mode["Auto"] = "auto";
    Mode["Heater"] = "heater";
    Mode["Cooler"] = "cooler";
})(Mode || (Mode = {}));
function loadAll() {
    loadTemperature();
    loadMode();
    loadTemps();
}
function getSync(path) {
    var ret = '';
    $.ajax({
        url: 'http://localhost:5000' + path,
        async: false,
        success: function (result) {
            ret = result;
        }
    });
    return ret;
}
function getTemperature() {
    return parseInt(getSync('/temperature'));
}
function getTemps() {
    return getSync('/temps').split(' ').map(function (x) { return parseInt(x); });
}
function getMode() {
    return Mode[getSync('/mode')];
}
function setTemps(temps) {
    var msg = temps.join(' ');
    $.post('/temps', msg);
}
function setMode(mode) {
    $.post('/mode', mode);
}
function loadTemperature() {
    $('#temperature-text').html(getTemperature() + '&deg;F');
}
function loadMode() {
    displayMode(getMode());
}
function displayMode(mode) {
    var modeStr = Mode[mode];
    $('.mode-btn').removeClass('active');
    $('#mode-' + modeStr).addClass('active');
}
function loadTemps() {
    window.temps = getTemps();
    displayTemps();
}
function displayTemps() {
    $('#left-temp-value').html(window.temps[0] + '&deg;F');
    $('#right-temp-value').html(window.temps[3] + '&deg;F');
}
