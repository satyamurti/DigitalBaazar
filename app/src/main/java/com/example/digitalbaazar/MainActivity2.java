package com.example.digitalbaazar;

import android.content.Intent;
import android.os.Bundle;
import android.widget.TextView;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.google.gson.Gson;

public class MainActivity2 extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main2);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;

        });

        Intent intent = getIntent();
        // receive the value by getStringExtra() method and
        // key must be same which is send by first activity
        String str = intent.getStringExtra("response");

        TextView title = findViewById(R.id.title);
        TextView price = findViewById(R.id.price);
        TextView description = findViewById(R.id.description);
        TextView brand = findViewById(R.id.brand);
        TextView category = findViewById(R.id.category);
        Gson gson = new Gson();

        System.out.println(str);
        SimpleEntity entity = gson.fromJson(str, SimpleEntity.class);

        title.setText(entity.title);
        price.setText(entity.price);
        description.setText(entity.description);
        brand.setText(entity.brand);
        category.setText(entity.category);
    }
}

class SimpleEntity {
    protected String title;
    protected String price;
    protected String description;
    protected String brand;
    protected String category;



    public SimpleEntity(String title, String price, String description, String brand, String category) {
        this.title = title;
        this.brand = brand;
        this.category = category;
        this.price = price;
        this.description = description;
    }

    // no-arg constructor, getters, and setters
}