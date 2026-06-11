<?php

namespace App\Mail;

use Illuminate\Bus\Queueable;
use Illuminate\Mail\Mailable;
use Illuminate\Mail\Mailables\Content;
use Illuminate\Mail\Mailables\Envelope;
use Illuminate\Queue\SerializesModels;

class TransactionCodeMail extends Mailable
{
    use Queueable, SerializesModels;

    public $code;
    public $amount;
    public $toAccount;
    public $description;

    /**
     * Create a new message instance.
     */
    public function __construct($code, $amount, $toAccount, $description)
    {
        $this->code = $code;
        $this->amount = $amount;
        $this->toAccount = $toAccount;
        $this->description = $description;
    }

    /**
     * Get the message envelope.
     */
    public function envelope(): Envelope
    {
        return new Envelope(
            subject: 'Transaction Authorization Code',
        );
    }

    /**
     * Get the message content definition.
     */
    public function content(): Content
    {
        return new Content(
            view: 'emails.transaction_code',
        );
    }

    /**
     * Get the attachments for the message.
     */
    public function attachments(): array
    {
        return [];
    }
}
