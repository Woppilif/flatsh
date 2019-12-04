BEGIN;
--
-- Add field ya_card_last4 to usersdocuments
--
ALTER TABLE "sharing_usersdocuments" ADD COLUMN "ya_card_last4" varchar(4) NULL;
--
-- Add field ya_card_type to usersdocuments
--
ALTER TABLE "sharing_usersdocuments" ADD COLUMN "ya_card_type" varchar(50) NULL;
COMMIT;
