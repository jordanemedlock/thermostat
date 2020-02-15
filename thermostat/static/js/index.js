var tempDelta = 2;
$(function () {
    loadAll();
    $(".mode-btn").click(function () {
        var id = $(this).attr('id');
        var mode = Mode[id.substr(5)];
        setMode(mode);
        displayMode(mode);
    });
    $('.left-temp-control .plus-btn').click(function () {
        window.temps[0] += 1;
        window.temps[1] = window.temps[0] + tempDelta;
        setTemps(window.temps);
        displayTemps();
    });
    $('.left-temp-control .minus-btn').click(function () {
        window.temps[0] -= 1;
        window.temps[1] = window.temps[0] + tempDelta;
        setTemps(window.temps);
        displayTemps();
    });
    $('.right-temp-control .plus-btn').click(function () {
        window.temps[3] += 1;
        window.temps[2] = window.temps[3] + tempDelta;
        setTemps(window.temps);
        displayTemps();
    });
    $('.right-temp-control .minus-btn').click(function () {
        window.temps[3] -= 1;
        window.temps[2] = window.temps[3] + tempDelta;
        setTemps(window.temps);
        displayTemps();
    });
});
var Mode;
(function (Mode) {
    Mode["off"] = "off";
    Mode["auto"] = "auto";
    Mode["heater"] = "heater";
    Mode["cooler"] = "cooler";
})(Mode || (Mode = {}));
function loadAll() {
    loadTemperature();
    loadMode();
    loadTemps();
}
function getSync(path) {
    var ret = '';
    $.ajax({
        url: path,
        async: false,
        success: function (result) {
            ret = result;
        }
    });
    return ret;
}
function getTemperature() {
    return (getSync('/temperature'));
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
    $.post('/mode/' + mode);
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
    $('#left-temp-value').html(window.temps[0] + '&deg;');
    $('#right-temp-value').html(window.temps[3] + '&deg;');
}
