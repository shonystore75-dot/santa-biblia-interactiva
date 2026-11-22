const config = {
  appId: 'com.diegoramirez.santabiblia',
  appName: 'Santa Biblia 2026',
  webDir: 'www',
  // Color de fondo nativo de la WebView: sin esto, Android la pinta de
  // blanco por defecto durante el instante antes de que cargue el CSS de
  // la página, lo cual se ve como un parpadeo blanco entre el video de
  // bienvenida y la app. Se usa negro puro porque es el color del video
  // del splash en ese último instante, para que el cambio sea invisible.
  backgroundColor: '#000000',
  plugins: {
    // Las páginas usan viewport-fit=cover (pantalla completa bajo la barra de estado
    // oculta): se avisa de antemano para evitar un salto de diseño al cargar.
    // style 'DARK' = íconos claros en las barras del sistema (el fondo es morado oscuro).
    SystemBars: { initialViewportFitValueHint: 'cover', style: 'DARK' },
  },
};

module.exports = config;
