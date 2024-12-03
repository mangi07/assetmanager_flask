import '@mdi/font/css/materialdesignicons.css' // Ensure you are using css-loader
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

const myCustomDarkTheme = {
  //dark: false,
  dark: true,
  colors: {
    background: '#121212',
    surface: '#212121',
    //surface: '#CF6679',
    'surface-bright': '#ccbfd6',
    'surface-variant': '#a3a3a3',
    'on-surface-variant': '#424242',
    primary: '#BB86FC',
    'primary-darken-1': '#3700B3',
    secondary: '#03DAC5',
    'secondary-darken-1': '#03DAC5',
    error: '#CF6679',
    info: '#2196F3',
    success: '#4CAF50',
    warning: '#FB8C00'
  },
  variables: {
    //'border-color': '#FFFFFF',
    'border-color': '#515151',
    'border-opacity': 0.12,
    //'high-emphasis-opacity': 1, // orig: This one is the problem! Plus v-list-item--active class, :hover, and :focus-visible are problematic
    //'high-emphasis-opacity': 0.40,
    'medium-emphasis-opacity': 0.70,
    //'medium-emphasis-opacity': 1,
    'disabled-opacity': 0.50,
    'idle-opacity': 0.10,
    'hover-opacity': 0.04, // orig
    //'hover-opacity': 1,
    //'hover-opacity': 0.80,
    'focus-opacity': 0.12, // orig
    //'focus-opacity': 1,
    //'focus-opacity': 0.80,
    'selected-opacity': 0.08, // orig
    //'selected-opacity': 1,
    //'selected-opacity': 0.80,
    'activated-opacity': 0.12, // orig
    //'activated-opacity': 1,
    'pressed-opacity': 0.16,
    'dragged-opacity': 0.08,
    'theme-kbd': '#212529',
    'theme-on-kbd': '#FFFFFF', // orig
    //'theme-on-kbd': '#111111',
    'theme-code': '#343434',
    'theme-on-code': '#CCCCCC' // orig
    //'theme-on-code': '#343434'
  }
}

export default createVuetify({
  theme: {
    //defaultTheme: 'dark'
    defaultTheme: 'myCustomDarkTheme',
    themes: {
      myCustomDarkTheme,
    },
  },
  //theme: false,
  icons: {
    defaultSet: 'mdi',
  },
  components,
  directives,
});

