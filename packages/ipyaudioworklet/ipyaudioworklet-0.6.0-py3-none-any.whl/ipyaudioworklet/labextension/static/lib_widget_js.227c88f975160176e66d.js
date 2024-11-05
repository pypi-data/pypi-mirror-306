"use strict";
(self["webpackChunk_naoh16_ipyaudioworklet"] = self["webpackChunk_naoh16_ipyaudioworklet"] || []).push([["lib_widget_js"],{

/***/ "./lib/audio.js":
/*!**********************!*\
  !*** ./lib/audio.js ***!
  \**********************/
/***/ (function(__unused_webpack_module, exports) {


var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.suspend = exports.resume = exports.getSampleRate = exports.run = exports.blob_url = exports.audiodata = void 0;
class DataViewEx extends DataView {
    setFourCC(offset, cc) {
        for (let i = 0; i < 4; i++) {
            this.setUint8(offset + i, cc.charCodeAt(i));
        }
    }
}
function encodeAudioAsWavfile(audiodata, settings) {
    // console.assert(settings.sampleSize == 16, "sampleSize (Bit-per-sample) should be 16.", settings);
    if (settings.sampleSize !== 16) {
        console.log('Warning: SampleSize is not 16 [bit].\n', 'The sound is forcely quantized as int16 (signed short) sound.', settings);
    }
    //console.assert(settings.channelCount == 1, "#Channel should be one (monoral).", settings);
    // @ts-ignore: TS2339
    if (settings.channelCount !== 1) {
        console.log('Warning: #Channel is not 1 (monoral).\n', 'The sound is forcely converted to monaural sound by "(L+R)/2" method.', settings);
    }
    // see WAVEFORMAT_EX
    // https://learn.microsoft.com/ja-jp/windows/win32/api/mmeapi/ns-mmeapi-waveformatex
    const _nSamplesPerSec = settings.sampleRate || 48000; // ex. 48000 [Hz]
    const _nChannels = 1; // settings.channelCount;   // ex. 1 [ch]
    const _wBitsPerSample = 16; // settings.sampleSize || 16;     // ex. 16 [bit]
    const _nBlockAlign = (_nChannels * _wBitsPerSample) / 8; // ex. 2 [byte]
    const _nAvgBytesPerSec = _nBlockAlign * _nSamplesPerSec; // ex. 96000 [byte/sec]
    const dataLengthSample = buffers.reduce((a, v) => a + v.length, 0);
    const dataLengthByte = dataLengthSample * _nBlockAlign;
    const arrayBuffer = new ArrayBuffer(44 + dataLengthByte);
    const dv = new DataViewEx(arrayBuffer);
    let offset = 0;
    // RIFF Header
    dv.setFourCC(offset, 'RIFF');
    offset += 4;
    dv.setUint32(offset, dataLengthByte + 36, true);
    offset += 4; // filesize - 8
    dv.setFourCC(offset, 'WAVE');
    offset += 4;
    // format chunk
    dv.setFourCC(offset, 'fmt ');
    offset += 4;
    dv.setUint32(offset, 16, true);
    offset += 4; // size = 16
    dv.setUint16(offset, 1, true);
    offset += 2; // WORD  wFormatTag
    dv.setUint16(offset, _nChannels, true);
    offset += 2; // WORD  nChannels
    dv.setUint32(offset, _nSamplesPerSec, true);
    offset += 4; // DWORD nSamplesPerSec
    dv.setUint32(offset, _nAvgBytesPerSec, true);
    offset += 4; // DWORD nAvgBytesPerSec
    dv.setUint16(offset, _nBlockAlign, true);
    offset += 2; // WORD  nBlockAlign
    dv.setUint16(offset, _wBitsPerSample, true);
    offset += 2; // WORD  wBitsPerSample
    // PCM-format neglect 'cbSize'
    // data chunk
    dv.setFourCC(offset, 'data');
    offset += 4;
    dv.setUint32(offset, dataLengthByte, true);
    offset += 4;
    for (const v of audiodata) {
        dv.setInt16(offset, Math.round(v * 32767), true);
        offset += 2;
    }
    console.log('Info: sampling_rate = ' +
        _nSamplesPerSec +
        ' length = ' +
        dataLengthSample +
        ', [sample]');
    return new Blob([dv], { type: 'audio/wav' });
}
const procdef_str = `class AudioRecorderProcessor extends AudioWorkletProcessor
{
  constructor() {
    super();
  }

  static get parameterDescriptors() {
    return [
      { name: "isRecording", defaultValue: 0 }
    ];
  }

  process(inputs, outputs, params) {
    if(!inputs[0][0]) return true;

    if(params.isRecording[0] > 0) {
      const firstInput = inputs[0];
      const firstOutput = outputs[0];
      const f2s_gain = 1. / firstInput.length;
      for(let n=0; n<firstInput.length; n++) {
        for(let m=0; m<firstInput[0].length; m++) {
          firstOutput[0][m] += firstInput[n][m] * f2s_gain;
        }
      }
      this.port.postMessage(firstOutput[0]);
    }

    return true;
  }
}
registerProcessor("audio-recorder-processor", AudioRecorderProcessor);`;
//const AudioContext = window.AudioContext || window.webkitAudioContext;
if (navigator.mediaDevices) {
    console.log('Info: getUserMedia is supported.');
}
else {
    console.log('Error: getUserMedia is not supported.');
}
let audioContext;
let audioRecorderNode; //AudioWorkletNode;
let audioSource;
let mediaConfig;
function prepareCustomAudioProcessor(module_url, module_name) {
    return __awaiter(this, void 0, void 0, function* () {
        if (!audioContext) {
            try {
                audioContext = new AudioContext();
                yield audioContext.suspend(); // or resume() ?
                yield audioContext.audioWorklet.addModule(module_url);
                audioRecorderNode = new AudioWorkletNode(audioContext, module_name);
                console.log(audioContext);
            }
            catch (e) {
                console.log(e);
                return null;
            }
        }
        return audioRecorderNode;
    });
}
function readyAudioSource(constraints = undefined) {
    return __awaiter(this, void 0, void 0, function* () {
        if (!audioSource) {
            try {
                if (!constraints) {
                    constraints = {
                        video: false,
                        audio: {
                            channelCount: { ideal: 1 } /** channelCount will be ignored... */,
                            sampleRate: { ideal: audioContext.sampleRate },
                            sampleSize: { ideal: 16 },
                            autoGainControl: false,
                            echoCancellation: false,
                            noiseSuppression: false,
                        },
                    };
                }
                const stream = yield navigator.mediaDevices.getUserMedia(constraints);
                audioSource = yield audioContext.createMediaStreamSource(stream);
                mediaConfig = yield stream.getAudioTracks()[0].getSettings();
                // Fix sampleRate
                mediaConfig.sampleRate =
                    mediaConfig.sampleRate || audioContext.sampleRate;
                console.log(stream);
                console.log(mediaConfig);
            }
            catch (e) {
                console.log(e);
                return null;
            }
        }
        return audioSource;
    });
}
let buffers = [];
exports.blob_url = '';
function run(annealing_time_ms = 500) {
    return __awaiter(this, void 0, void 0, function* () {
        console.log('(1)');
        const blob = new Blob([procdef_str], { type: 'application/javascript' });
        yield prepareCustomAudioProcessor(URL.createObjectURL(blob), 'audio-recorder-processor');
        console.log(audioRecorderNode);
        console.log('(2)');
        yield readyAudioSource();
        console.log('(3)');
        yield audioSource.connect(audioRecorderNode);
        console.log('(4)');
        yield audioContext.resume();
        yield setTimeout(() => {
            audioContext.suspend();
        }, annealing_time_ms);
        // In general, most of the recording device could not record just after the device booted up.
        // Short wait will be make better result for the first take of recording.
        return;
    });
}
exports.run = run;
function getSampleRate() {
    return mediaConfig.sampleRate || audioContext.sampleRate;
}
exports.getSampleRate = getSampleRate;
function resume(cb_func) {
    buffers = [];
    audioRecorderNode.port.onmessage = (e) => {
        buffers.push(e.data);
        if (cb_func)
            cb_func(e.data);
    };
    audioContext.resume();
    audioRecorderNode.parameters
        .get('isRecording')
        .setValueAtTime(1, audioContext.currentTime);
    console.log('recording');
}
exports.resume = resume;
function suspend() {
    audioContext.suspend();
    audioRecorderNode.parameters
        .get('isRecording')
        .setValueAtTime(0, audioContext.currentTime);
    console.log('suspended');
    const dataLengthSample = buffers.reduce((a, v) => a + v.length, 0);
    exports.audiodata = new Array(dataLengthSample);
    let offset = 0;
    for (const buffer of buffers) {
        for (const value of buffer) {
            exports.audiodata[offset++] = value;
        }
    }
    const blob = encodeAudioAsWavfile(exports.audiodata, mediaConfig);
    console.log(blob);
    exports.blob_url = URL.createObjectURL(blob);
    //       var reader = new FileReader();
    //       reader.readAsDataURL(blob);
    //       reader.onloadend = function() {
    //         var base64data = reader.result;
    //         const uiLog = document.querySelector('div#log');
    //         uiLog.innerHTML += '<div style="width:100%; overflow-wrap: anywhere;"><code>' + base64data + '</code></div>';
    //       }
}
exports.suspend = suspend;


/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


// Copyright (c) Sunao Hara
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


// Copyright (c) Sunao Hara
// Distributed under the terms of the Modified BSD License.
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.AudioRecorderView = exports.AudioRecorderModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base?ea51");
const jupyter_dataserializers_1 = __webpack_require__(/*! jupyter-dataserializers */ "webpack/sharing/consume/default/jupyter-dataserializers/jupyter-dataserializers");
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
const a = __importStar(__webpack_require__(/*! ./audio */ "./lib/audio.js"));
// Import the CSS
//import '../css/widget.css';
class AudioRecorderModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: AudioRecorderModel.model_name, _model_module: AudioRecorderModel.model_module, _model_module_version: AudioRecorderModel.model_module_version, _view_name: AudioRecorderModel.view_name, _view_module: AudioRecorderModel.view_module, _view_module_version: AudioRecorderModel.view_module_version, value: 'Audio Recorder', audiodata: new Float32Array(0), audiochunk: new Float32Array(0), blob_url: '', filename: 'default.wav', status: 'NOT_INITIALIZED' });
    }
}
exports.AudioRecorderModel = AudioRecorderModel;
AudioRecorderModel.serializers = Object.assign(Object.assign({}, base_1.DOMWidgetModel.serializers), { audiodata: jupyter_dataserializers_1.simplearray_serialization, audiochunk: jupyter_dataserializers_1.simplearray_serialization });
AudioRecorderModel.model_name = 'AudioRecorderModel';
AudioRecorderModel.model_module = version_1.MODULE_NAME;
AudioRecorderModel.model_module_version = version_1.MODULE_VERSION;
AudioRecorderModel.view_name = 'AudioRecorderView'; // Set to null if no view
AudioRecorderModel.view_module = version_1.MODULE_NAME; // Set to null if no view
AudioRecorderModel.view_module_version = version_1.MODULE_VERSION;
class AudioRecorderView extends base_1.DOMWidgetView {
    constructor() {
        super(...arguments);
        this._useAudiochunk = false;
    }
    render() {
        this.el.classList.add('jupyter-widgets');
        this._message = document.createElement('div');
        this.el.appendChild(this._message);
        this._bootButton = document.createElement('button');
        this._bootButton.classList.add('jupyter-widgets', 'jupyter-button', 'widget-button');
        this._bootButton.textContent = 'Boot RECORDER';
        this._bootButton.title = 'run()';
        this.el.appendChild(this._bootButton);
        this._resumeButton = document.createElement('button');
        this._resumeButton.classList.add('jupyter-widgets', 'jupyter-button', 'widget-button');
        this._resumeButton.disabled = true;
        this._resumeButton.textContent = 'Record';
        this._resumeButton.title = 'resume()';
        this.el.appendChild(this._resumeButton);
        this._suspendButton = document.createElement('button');
        this._suspendButton.classList.add('jupyter-widgets', 'jupyter-button', 'widget-button');
        this._suspendButton.disabled = true;
        this._suspendButton.textContent = 'Stop';
        this._suspendButton.title = 'suspend()';
        this.el.appendChild(this._suspendButton);
        this._audioControl = document.createElement('audio');
        this._audioControl.controls = true;
        this.el.appendChild(this._audioControl);
        this.value_changed();
        // Python --> JavaScipt update
        this.model.on('change:value', this.value_changed, this);
        this.model.on('msg:custom', this.on_msg, this);
        // JavaScipt --> Python update
        this._bootButton.onclick = this._onClickBootButton.bind(this);
        this._resumeButton.onclick = this._onClickResumeButton.bind(this);
        this._suspendButton.onclick = this._onClickSuspendButton.bind(this);
    }
    value_changed() {
        this._message.textContent = this.model.get('value');
    }
    on_msg(command, buffers) {
        switch (command.cmd) {
            case 'run':
                this._onClickBootButton();
                break;
            case 'resume':
                this._onClickResumeButton();
                break;
            case 'suspend':
                this._onClickSuspendButton();
                break;
            case 'use_audiochunk':
                this._useAudiochunk = command.args[0];
                break;
        }
    }
    _onClickBootButton() {
        this.model.set('value', 'AudioRecorder is booting...');
        this.model.set('status', 'INITIALIZING');
        this.model.save_changes();
        a.run().then((r) => {
            const _sampleRate = a.getSampleRate() || -1;
            this.model.set('value', 'AudioRecorder is ready (Sampling rate: ' +
                String(_sampleRate) +
                ' Hz).');
            this.model.set('status', 'READY');
            this.model.set('sampleRate', _sampleRate);
            this.model.save_changes();
            this._bootButton.disabled = true;
            this._resumeButton.disabled = false;
        });
    }
    _onClickResumeButton() {
        if (this._useAudiochunk) {
            a.resume((datachunk) => {
                this.model.set('audiochunk', {
                    array: new Float32Array(datachunk),
                    shape: [datachunk.length]
                });
                this.model.save_changes();
            });
        }
        else {
            a.resume(undefined);
        }
        this.model.set('value', this._message.textContent + ' [RESUME]');
        this.model.set('status', 'RECORDING');
        this.model.save_changes();
        this._resumeButton.disabled = true;
        this._suspendButton.disabled = false;
    }
    _onClickSuspendButton() {
        a.suspend();
        // console.log(a.audiodata);
        this.model.set('audiodata', {
            array: new Float32Array(a.audiodata),
            shape: [a.audiodata.length]
        });
        this.model.set('blob_url', a.blob_url);
        this.model.set('value', this._message.textContent + ' [SUSPEND]');
        this.model.set('status', 'RECORDED');
        this.model.save_changes();
        this._audioControl.src = a.blob_url;
        this._audioControl.title = this.model.get('filename');
        this._resumeButton.disabled = false;
        this._suspendButton.disabled = true;
    }
}
exports.AudioRecorderView = AudioRecorderView;


/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

module.exports = /*#__PURE__*/JSON.parse('{"name":"@naoh16/ipyaudioworklet","version":"0.6.0","description":"A Jupyter Widget for Web Audio Recording using Audio Worklet","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/naoh16/ipyaudioworklet","bugs":{"url":"https://github.com/naoh16/ipyaudioworklet/issues"},"license":"BSD-3-Clause","author":{"name":"Sunao Hara","email":"sunao.hara@gmail.com"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/naoh16/ipyaudioworklet"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev && yarn run build:postprocess","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension && yarn run build:postprocess","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","build:postprocess":"node build-post-process.js","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf ipyaudioworklet/labextension","clean:nbextension":"rimraf ipyaudioworklet/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2 || ^3 || ^4 || ^5 || ^6","@jupyterlab/application":"~4.2.5","jupyter-dataserializers":"^2.1.0"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyter-widgets/base-manager":"^1.0.2","@jupyterlab/builder":">=3.0.0","@lumino/application":"^1.6.0","@lumino/widgets":"^1.6.0","@types/audioworklet":"^0.0.50","@types/jest":"^28.0.0","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","copy-webpack-plugin":"^11.0.0","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^28.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^28.0.0","ts-loader":"^8.0.0","typescript":"~4.5.0","webpack":"^5.61.0","webpack-cli":"^4.0.0","write-file-webpack-plugin":"^4.5.1"},"jupyterlab":{"extension":"lib/plugin","outputDir":"ipyaudioworklet/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js.227c88f975160176e66d.js.map