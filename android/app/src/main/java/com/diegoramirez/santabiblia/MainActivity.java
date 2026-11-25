package com.diegoramirez.santabiblia;

import android.graphics.Bitmap;
import android.graphics.Color;
import android.graphics.Rect;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.Gravity;
import android.view.PixelCopy;
import android.view.View;
import android.webkit.JavascriptInterface;
import android.webkit.WebChromeClient;
import android.webkit.WebView;
import android.widget.ImageView;
import androidx.activity.OnBackPressedCallback;
import com.getcapacitor.Bridge;
import com.getcapacitor.BridgeWebChromeClient;
import com.getcapacitor.WebViewListener;
import android.view.Window;
import android.view.WindowManager;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.core.view.WindowInsetsControllerCompat;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.VideoView;
import com.getcapacitor.BridgeActivity;

/**
 * La app arranca directamente aquí (no hay una pantalla separada para el
 * video). El video de bienvenida se muestra como una capa flotando encima
 * de la propia pantalla principal mientras esta carga la Biblia por detrás
 * en silencio. Así, cuando el video termina, el contenido ya está listo y
 * no hay ninguna espera ni pantalla en blanco/negra de por medio.
 */
public class MainActivity extends BridgeActivity {

    // Red de seguridad: si el video no carga, falla, o tarda demasiado,
    // igual se quita y se ve la app, para que nunca se quede trabada.
    private static final int TIEMPO_MAXIMO_MS = 6000;

    private final Handler handler = new Handler(Looper.getMainLooper());
    private boolean yaSeQuito = false;
    private FrameLayout capaVideo;

    // Pantalla completa de elementos web (el reproductor de YouTube de las historias).
    private FrameLayout contenedorPantallaCompleta;
    private WebChromeClient.CustomViewCallback callbackPantallaCompleta;
    private OnBackPressedCallback atrasPantallaCompleta;

    // Transición entre pantallas: foto de la pantalla anterior encima de la WebView mientras carga la nueva.
    private static final int ESPERA_MAXIMA_TRANSICION_MS = 1500;
    private static final int FUNDIDO_MS = 140;
    private ImageView capaTransicion;
    private final Runnable finTransicion = this::fundirTransicion;

    // Paleta Marfil clásico (barra inferior clara): los iconos de la barra de navegación del sistema deben ser oscuros.
    private volatile boolean navegacionClara = false;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        // Importante: se llama a super primero. Capacitor cambia aquí el tema de
        // arranque por uno sin barra de acción; si la ventana se tocara antes, se
        // crearía con el tema de arranque y quedaría una barra de acción negra arriba.
        super.onCreate(savedInstanceState);

        // Pantalla completa: la app se dibuja hasta el borde superior (y bajo la
        // muesca/cámara frontal), y solo se oculta la barra de estado. La barra de
        // navegación de abajo con los botones de Android se deja visible.
        Window ventana = getWindow();
        WindowCompat.setDecorFitsSystemWindows(ventana, false);
        if (android.os.Build.VERSION.SDK_INT >= 28) {
            WindowManager.LayoutParams atributos = ventana.getAttributes();
            atributos.layoutInDisplayCutoutMode = WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES;
            ventana.setAttributes(atributos);
        }
        ocultarBarraDeEstado();
        // El plugin SystemBars de Capacitor muestra las barras al iniciar; se vuelve
        // a ocultar justo después para que gane esta configuración.
        handler.post(this::ocultarBarraDeEstado);
        mostrarVideoDeBienvenida();
        configurarPantallaCompletaWeb();
        configurarPuenteTema();
        configurarTransiciones();
    }

    /**
     * Cada pantalla es una página distinta y su primer fotograma sale antes que las imágenes, las fuentes
     * y el contenido. Para que no se vea a medio pintar, al empezar la carga se deja encima una copia de
     * lo que había y se funde cuando la página nueva avisa (AndroidTema.pantallaLista en temas.js).
     */
    private void configurarTransiciones() {
        Bridge puente = getBridge();
        if (puente == null) return;
        puente.addWebViewListener(new WebViewListener() {
            @Override
            public void onPageStarted(WebView web) {
                conservarPantalla(web);
            }
        });
    }

    private void conservarPantalla(WebView web) {
        // Sin copia durante el video de bienvenida o un video a pantalla completa (PixelCopy existe desde Android 8).
        if (android.os.Build.VERSION.SDK_INT < 26 || capaVideo != null || contenedorPantallaCompleta != null) return;
        handler.removeCallbacks(finTransicion);
        handler.postDelayed(finTransicion, ESPERA_MAXIMA_TRANSICION_MS);
        if (capaTransicion != null) {
            // Segundo cambio antes de terminar el primero: se mantiene (y se vuelve a mostrar entera) la copia que ya está.
            capaTransicion.animate().cancel();
            capaTransicion.setAlpha(1f);
            return;
        }
        int ancho = web.getWidth(), alto = web.getHeight();
        if (!web.isShown() || ancho == 0 || alto == 0) return;
        ViewGroup raiz = findViewById(android.R.id.content);
        int[] enVentana = new int[2], origenRaiz = new int[2];
        web.getLocationInWindow(enVentana);
        raiz.getLocationInWindow(origenRaiz);
        Bitmap foto = Bitmap.createBitmap(ancho, alto, Bitmap.Config.ARGB_8888);
        ImageView capa = new ImageView(this);
        capaTransicion = capa;
        Rect zona = new Rect(enVentana[0], enVentana[1], enVentana[0] + ancho, enVentana[1] + alto);
        PixelCopy.request(getWindow(), zona, foto, resultado -> {
            if (capaTransicion != capa) return;
            if (resultado != PixelCopy.SUCCESS) {
                capaTransicion = null;
                return;
            }
            capa.setImageBitmap(foto);
            FrameLayout.LayoutParams lugar = new FrameLayout.LayoutParams(ancho, alto);
            lugar.leftMargin = enVentana[0] - origenRaiz[0];
            lugar.topMargin = enVentana[1] - origenRaiz[1];
            raiz.addView(capa, lugar);
        }, handler);
    }

    private void fundirTransicion() {
        handler.removeCallbacks(finTransicion);
        final ImageView capa = capaTransicion;
        if (capa == null) return;
        if (capa.getParent() == null) {
            capaTransicion = null;
            return;
        }
        capa.animate().alpha(0f).setDuration(FUNDIDO_MS).withEndAction(() -> {
            ((ViewGroup) capa.getParent()).removeView(capa);
            if (capaTransicion == capa) capaTransicion = null;
        });
    }

    /** Puente JS -> nativo: la web (temas.js) avisa de la paleta activa para elegir iconos claros u oscuros en la barra de navegación. */
    private class PuenteTema {
        @JavascriptInterface
        public void pantallaLista() {
            runOnUiThread(MainActivity.this::alEstarListaLaPantalla);
        }

        @JavascriptInterface
        public void barraNavegacionClara(final boolean clara) {
            runOnUiThread(() -> {
                navegacionClara = clara;
                ocultarBarraDeEstado();
            });
        }
    }

    private void alEstarListaLaPantalla() {
        Bridge puente = getBridge();
        if (puente == null || puente.getWebView() == null || capaTransicion == null) return;
        // Espera a que lo ya dibujado por la página esté realmente en pantalla antes de descubrirlo.
        puente.getWebView().postVisualStateCallback(0, new WebView.VisualStateCallback() {
            @Override
            public void onComplete(long id) {
                fundirTransicion();
            }
        });
    }

    private void configurarPuenteTema() {
        Bridge puente = getBridge();
        if (puente == null || puente.getWebView() == null) return;
        puente.getWebView().addJavascriptInterface(new PuenteTema(), "AndroidTema");
        // Si la primera página empezó a cargar antes de registrar el puente, se le pide que vuelva a avisar.
        handler.postDelayed(this::pedirTemaALaWeb, 1200);
    }

    private void pedirTemaALaWeb() {
        Bridge puente = getBridge();
        if (puente == null || puente.getWebView() == null) return;
        puente.getWebView().evaluateJavascript("window.aplicarTema&&window.temaActual&&window.aplicarTema(window.temaActual())", null);
    }

    /**
     * El cliente por defecto de Capacitor rechaza al instante cualquier pantalla completa
     * (llama a onCustomViewHidden). Este la acepta: pone la vista a pantalla completa sobre la
     * app, oculta las dos barras del sistema, y el botón Atrás la cierra antes que nada.
     */
    private void configurarPantallaCompletaWeb() {
        Bridge puente = getBridge();
        if (puente == null || puente.getWebView() == null) return;
        puente.getWebView().setWebChromeClient(new BridgeWebChromeClient(puente) {
            @Override
            public void onShowCustomView(View vista, WebChromeClient.CustomViewCallback callback) {
                mostrarPantallaCompleta(vista, callback);
            }

            @Override
            public void onHideCustomView() {
                ocultarPantallaCompleta();
            }
        });
        atrasPantallaCompleta = new OnBackPressedCallback(false) {
            @Override
            public void handleOnBackPressed() {
                if (callbackPantallaCompleta != null) callbackPantallaCompleta.onCustomViewHidden();
                ocultarPantallaCompleta();
            }
        };
        getOnBackPressedDispatcher().addCallback(this, atrasPantallaCompleta);
    }

    private void mostrarPantallaCompleta(View vista, WebChromeClient.CustomViewCallback callback) {
        if (contenedorPantallaCompleta != null) {
            callback.onCustomViewHidden();
            return;
        }
        ViewGroup raiz = findViewById(android.R.id.content);
        contenedorPantallaCompleta = new FrameLayout(this);
        contenedorPantallaCompleta.setBackgroundColor(Color.BLACK);
        contenedorPantallaCompleta.addView(
            vista,
            new FrameLayout.LayoutParams(FrameLayout.LayoutParams.MATCH_PARENT, FrameLayout.LayoutParams.MATCH_PARENT)
        );
        raiz.addView(
            contenedorPantallaCompleta,
            new ViewGroup.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT)
        );
        callbackPantallaCompleta = callback;
        if (atrasPantallaCompleta != null) atrasPantallaCompleta.setEnabled(true);

        Window ventana = getWindow();
        WindowInsetsControllerCompat controlador = WindowCompat.getInsetsController(ventana, ventana.getDecorView());
        controlador.setSystemBarsBehavior(WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
        controlador.hide(WindowInsetsCompat.Type.systemBars());
    }

    private void ocultarPantallaCompleta() {
        if (contenedorPantallaCompleta == null) return;
        ViewGroup padre = (ViewGroup) contenedorPantallaCompleta.getParent();
        if (padre != null) padre.removeView(contenedorPantallaCompleta);
        contenedorPantallaCompleta.removeAllViews();
        contenedorPantallaCompleta = null;
        callbackPantallaCompleta = null;
        if (atrasPantallaCompleta != null) atrasPantallaCompleta.setEnabled(false);
        // Vuelve el comportamiento normal de la app: barra de estado oculta, barra de navegación visible.
        ocultarBarraDeEstado();
    }

    @Override
    public void onResume() {
        super.onResume();
        ocultarBarraDeEstado();
        pedirTemaALaWeb();
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) ocultarBarraDeEstado();
    }

    /** Oculta solo la barra de estado y deja la de navegación con íconos claros; al deslizar desde arriba aparece un momento y se vuelve a ir. */
    private void ocultarBarraDeEstado() {
        Window ventana = getWindow();
        WindowInsetsControllerCompat controlador = WindowCompat.getInsetsController(ventana, ventana.getDecorView());
        controlador.setSystemBarsBehavior(WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
        controlador.hide(WindowInsetsCompat.Type.statusBars());
        controlador.show(WindowInsetsCompat.Type.navigationBars());
        // Íconos de la barra de navegación: claros salvo en Marfil clásico (menú inferior claro), donde son oscuros.
        // Barra transparente: se ve el color del menú de la app y Xiaomi respeta la elección de íconos
        // (con el color por defecto de la barra los pintaba oscuros aunque se pidieran claros).
        ventana.setNavigationBarColor(Color.TRANSPARENT);
        controlador.setAppearanceLightNavigationBars(navegacionClara);
        if (android.os.Build.VERSION.SDK_INT >= 29) {
            ventana.setNavigationBarContrastEnforced(false);
        }
    }

    private void mostrarVideoDeBienvenida() {
        ViewGroup raiz = findViewById(android.R.id.content);

        capaVideo = new FrameLayout(this);
        capaVideo.setBackgroundColor(Color.BLACK);
        raiz.addView(
            capaVideo,
            new ViewGroup.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT)
        );

        VideoView video = new VideoView(this);
        FrameLayout.LayoutParams parametrosVideo = new FrameLayout.LayoutParams(
            FrameLayout.LayoutParams.MATCH_PARENT,
            FrameLayout.LayoutParams.MATCH_PARENT
        );
        parametrosVideo.gravity = Gravity.CENTER;
        capaVideo.addView(video, parametrosVideo);

        try {
            Uri uriVideo = Uri.parse("android.resource://" + getPackageName() + "/" + R.raw.splash_video);
            video.setVideoURI(uriVideo);
            video.setOnCompletionListener(mp -> quitarVideo());
            video.setOnErrorListener((mp, what, extra) -> {
                quitarVideo();
                return true;
            });
            video.start();
        } catch (Exception e) {
            quitarVideo();
        }

        handler.postDelayed(this::quitarVideo, TIEMPO_MAXIMO_MS);
    }

    private synchronized void quitarVideo() {
        if (yaSeQuito) return;
        yaSeQuito = true;
        handler.removeCallbacksAndMessages(null);
        if (capaVideo != null) {
            ViewGroup padre = (ViewGroup) capaVideo.getParent();
            if (padre != null) {
                padre.removeView(capaVideo);
            }
            capaVideo = null;
        }
        pedirTemaALaWeb();
    }

    @Override
    public void onDestroy() {
        handler.removeCallbacksAndMessages(null);
        super.onDestroy();
    }
}
