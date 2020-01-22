$(function() {
  loadAll();

  $(".mode-btn").click(function(){
      let id = $(this).attr('id');
      let mode = Mode[id.substr(5)]
      setMode(mode);
      displayMode(mode);
  });
});


interface Window { temps: Array<number>; }

enum Mode {
  Off = 'off',
  Auto = 'auto',
  Heater = 'heater',
  Cooler = 'cooler'
}

function loadAll() {
  loadTemperature();
  loadMode();
  loadTemps();
}

function getSync(path: string): string {
  var ret: string = '';
  $.ajax({
    url: 'http://localhost:5000' + path,
    async: false,
    success: function(result) {
      ret = result;
    }
  })
  return ret;
}

function getTemperature(): number {
  return parseInt(getSync('/temperature'));
}

function getTemps(): Array<number> {
  return getSync('/temps').split(' ').map((x) => parseInt(x));
}

function getMode(): Mode {
  return Mode[getSync('/mode')];
}

function setTemps(temps: Array<number>) {
  let msg = temps.join(' ');
  $.post('/temps', msg);
}

function setMode(mode: Mode) {
  $.post('/mode', mode);
}


function loadTemperature() {
  $('#temperature-text').html(getTemperature() + '&deg;F');
}

function loadMode() {
  displayMode(getMode());
}

function displayMode(mode: Mode) {
  let modeStr = Mode[mode];
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

