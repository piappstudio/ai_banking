<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reset Your Password - AI Banking</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
            background-color: #f4f7f6;
        }
        .container {
            max-width: 600px;
            margin: 40px auto;
            background: #ffffff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }
        .header {
            background-color: #2c3e50;
            color: #ffffff;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
            letter-spacing: 1px;
        }
        .content {
            padding: 40px;
            text-align: center;
        }
        .greeting {
            font-size: 18px;
            margin-bottom: 20px;
            color: #555;
        }
        .instruction {
            margin-bottom: 30px;
        }
        .otp-container {
            background-color: #f0f4f8;
            border: 2px dashed #2c3e50;
            border-radius: 12px;
            padding: 20px;
            margin: 30px 0;
            display: inline-block;
        }
        .otp-code {
            font-size: 36px;
            font-weight: bold;
            color: #2c3e50;
            letter-spacing: 8px;
            margin: 0;
        }
        .expiry {
            font-size: 14px;
            color: #888;
            margin-top: 20px;
        }
        .footer {
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #aaa;
            background-color: #fafafa;
            border-top: 1px solid #eee;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AI Banking</h1>
        </div>
        <div class="content">
            <div class="greeting">Reset Your Password</div>
            <p class="instruction">We received a request to reset your password. Please use the following 6-digit verification code to proceed:</p>

            <div class="otp-container">
                <p class="otp-code">{{ $code }}</p>
            </div>

            <p class="expiry">This code is valid for <strong>1 hour</strong>. If you didn't request a password reset, you can safely ignore this email.</p>
        </div>
        <div class="footer">
            &copy; {{ date('Y') }} AI Banking. Secure Banking for the Modern World.
        </div>
    </div>
</body>
</html>
