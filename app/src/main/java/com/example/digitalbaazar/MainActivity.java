package com.example.digitalbaazar;

import android.Manifest;
import android.app.Notification;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.os.StrictMode;
import android.provider.MediaStore;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.OnProgressListener;
import com.google.firebase.storage.StorageReference;
import com.google.firebase.storage.UploadTask;

import java.io.ByteArrayOutputStream;
import java.io.Console;
import java.io.IOException;

import okhttp3.FormBody;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {

    // Define the pic id
    private static final int pic_id = 123;
    public String uploadedImageUrl = "";
    ImageView click_image_id;
    ProgressBar progressBar;
    TextView progressBarTextView;
    Button scanProductButton;
    Bitmap photo;
    Uri fileUri;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);

        scanProductButton = findViewById(R.id.scan_product_button);
        click_image_id = findViewById(R.id.click_image);
        progressBar = findViewById(R.id.progressBar);
        progressBarTextView = findViewById(R.id.progressTextView);
//        FirebaseStorage storage = FirebaseStorage.getInstance();

        if (android.os.Build.VERSION.SDK_INT > 9) {
            StrictMode.ThreadPolicy gfgPolicy =
                    new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(gfgPolicy);
        }


        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        if (ContextCompat.checkSelfPermission(this, android.Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{android.Manifest.permission.WRITE_EXTERNAL_STORAGE}, 1);
        }



        scanProductButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {

                if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
                    ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.CAMERA}, 1);
                }
                // Create the camera_intent ACTION_IMAGE_CAPTURE it will open the camera for capture the image
                Intent camera_intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                // Start the activity with camera_intent, and request pic id
                startActivityForResult(camera_intent, pic_id);

            }
        });
    }

    private void UploadToFireStore(Bitmap photu) {
        StorageReference storageRef = FirebaseStorage.getInstance().getReference();

        ByteArrayOutputStream bytes = new ByteArrayOutputStream();
        photu.compress(Bitmap.CompressFormat.JPEG, 100, bytes);
        String path = MediaStore.Images.Media.insertImage(MainActivity.this.getContentResolver(), photu, "Title", null);

        fileUri = Uri.parse(path);

        StorageReference uploadImageRef = storageRef.child("images/"+fileUri.getLastPathSegment());

        UploadTask uploadTask = uploadImageRef.putFile(fileUri);

        uploadTask.addOnSuccessListener(new OnSuccessListener<UploadTask.TaskSnapshot>() {
            @Override
            public void onSuccess(UploadTask.TaskSnapshot taskSnapshot) {
                taskSnapshot.getStorage().getDownloadUrl().addOnCompleteListener(new OnCompleteListener<Uri>() {
                    @Override
                    public void onComplete(@NonNull Task<Uri> task) {
                        uploadedImageUrl = task.getResult().toString();
                        Toast.makeText(MainActivity.this, "File Url" + uploadedImageUrl, Toast.LENGTH_SHORT).show();
//                        UploadToFlask(uploadedImageUrl);
//                        String res = new background(uploadedImageUrl).execute();


                        final String[] str = {""};
                        Thread gfgThread = new Thread(new Runnable() {
                            @Override
                            public void run() {
                                try  {
                                    str[0] = UploadToFlask(uploadedImageUrl);
                                } catch (Exception e) {
                                    e.printStackTrace();
                                }
                            }
                        });

                        gfgThread.start();
                        try {
                            gfgThread.join();
                        } catch (InterruptedException e) {
                            throw new RuntimeException(e);
                        }

                        Intent intent = new Intent(getApplicationContext(), MainActivity2.class);
                        // now by putExtra method put the value in key, value pair key is
                        // message_key by this key we will receive the value, and put the string
                        intent.putExtra("response", uploadedImageUrl);
                        // start the Intent
                        startActivity(intent);
                    }
                });
            }
        }).addOnFailureListener(new OnFailureListener() {
            @Override
            public void onFailure(@NonNull Exception e) {
                Toast.makeText(MainActivity.this, "Upload failed due to some reason", Toast.LENGTH_SHORT).show();

            }
        }).addOnProgressListener(new OnProgressListener<UploadTask.TaskSnapshot>() {
            @Override
            public void onProgress(@NonNull UploadTask.TaskSnapshot taskSnapshot) {
                double progress = (100.0 * taskSnapshot.getBytesTransferred()) / taskSnapshot.getTotalByteCount();

                progressBar.setProgress((int) progress);
                String progressString = ((int) progress) + "% done";
                progressBarTextView.setText(progressString);
            }
        });
    }


    private String UploadToFlask(String url){
        OkHttpClient client = new OkHttpClient().newBuilder()
                .build();
        MediaType mediaType = MediaType.parse("application/json");
        RequestBody body = RequestBody.create(mediaType, "{\n    \"key\": \"" + url + "\"\n}");
        Request request = new Request.Builder()
                .url("http://20.203.40.255:8080/1/add_inventory/upload_image_url")
                .method("POST", body)
                .addHeader("Content-Type", "application/json")
                .build();
        try {
            Response response = client.newCall(request).execute();
//            Intent intent = new Intent(getApplicationContext(), MainActivity2.class);
//            // now by putExtra method put the value in key, value pair key is
//            // message_key by this key we will receive the value, and put the string
//            intent.putExtra("response", response.body().toString());
//            // start the Intent
//            startActivity(intent);

            return response.body().toString();
        } catch (IOException e) {
            e.printStackTrace();
        }
//        Unirest.setTimeouts(0, 0);
//        HttpResponse<String> response = Unirest.post("http://20.203.40.255:8080/1/add_inventory/upload_image_url")
//                .header("Content-Type", "application/x-www-form-urlencoded")
//                .field("url", url)
//                .asString();
//        return response;
        return "";
    }

    // This method will help to retrieve the image
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        // Match the request 'pic id with requestCode
        if (requestCode == pic_id) {
            // BitMap is data structure of image file which store the image in memory
            photo = (Bitmap) data.getExtras().get("data");
            // Set the image in imageview for display
            click_image_id.setImageBitmap(photo);
            scanProductButton.setVisibility(View.GONE);


            UploadToFireStore(photo);
        }
    }

    private Uri getImageUri(Context context, Bitmap inImage) {
        ByteArrayOutputStream bytes = new ByteArrayOutputStream();
        inImage.compress(Bitmap.CompressFormat.JPEG, 100, bytes);
        String path = MediaStore.Images.Media.insertImage(context.getContentResolver(), inImage, "Title", null);
        return Uri.parse(path);
    }

}

//public class OkHttpHandler extends AsyncTask {
//
//    OkHttpClient client = new OkHttpClient();
//
//    @Override
//    protected String doInBackground(String...params) {
//
//        Request.Builder builder = new Request.Builder();
//        builder.url(params[0]);
//        Request request = builder.build();
//
//        try {
//            Response response = client.newCall(request).execute();
//            return response.body().string();
//        }catch (Exception e){
//            e.printStackTrace();
//        }
//        return null;
//    }
//
//    @Override
//    protected void onPostExecute(String s) {
//        super.onPostExecute(s);
//        txtString.setText(s);
//    }
//}