package com.diegoramirez.santabiblia;

import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.Gravity;
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

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mostrarVideoDeBienvenida();
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
    }

    @Override
    public void onDestroy() {
        handler.removeCallbacksAndMessages(null);
        super.onDestroy();
    }
}
