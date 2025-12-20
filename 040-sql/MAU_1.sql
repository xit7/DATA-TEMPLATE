
-- Build a user-level dataset for Monthly Active Users (MAU)
SELECT
    silver.user_id,                                -- Unique user identifier
    silver.application,                            -- Application name
    COALESCE(b2b.ech_parent_name, b2b.org_name) AS org_parent_name, -- Parent org name if available
    b2b.industry,                                  -- Industry classification
    b2b.ech_sub_industry,                          -- Sub-industry classification

    -- Flag: true if asset type is 'kwc' or 'project'
    CASE WHEN construct.asset_type IN ('kwc', 'project') THEN true ELSE false END AS is_project_kwc_asset_type,

    b2b.org_name,                                  -- Organisation name
    am.Product,                                    -- Product mapped from application
    am.Product_Group,                              -- Product group
    silver.construct.asset_class,                  -- Asset class

    -- Normalise asset directory type for readability
    CASE WHEN silver.construct.asset_directory_type = 'kwc'
         THEN 'Knowledge Workspace'
         ELSE initcap(silver.construct.asset_directory_type)
    END AS asset_directory_type,

    -- Flag: GenAI user or custom model asset type
    CASE WHEN (silver.is_genai_user = true) OR silver.construct.asset_type = 'cm'
         THEN true ELSE false
    END AS is_genai_user,

    silver.construct.is_cloud_doc,                 -- Whether asset is a cloud doc

    -- Normalise asset type into readable construct names
    CASE
        WHEN lower(silver.construct.asset_type) LIKE '%assignment%' THEN 'Assignment'
        WHEN silver.construct.asset_type = 'kwc' THEN 'Knowledge Workspace'
        WHEN silver.construct.asset_type IN ('cm_training_set', 'cm') THEN 'Custom Model'
        ELSE initcap(silver.construct.asset_type)
    END AS construct,

    silver.Is_Collab_User,                         -- Collaboration flag
    silver.Is_HIU,                                 -- High-Intent User flag
    silver.days_active,                            -- Number of active days

    -- Convert RETURN to REPEAT for user type
    CASE WHEN silver.User_Type_Overall = 'RETURN' THEN 'REPEAT'
         ELSE silver.User_Type_Overall
    END AS User_Type,

    silver.User_Type_App_Level,                   -- App-level user type
    silver.event_initiation_type,                 -- How the event was initiated
    silver.total_events,                          -- Total events count
    silver.crud_events,                           -- CRUD events count
    silver.invitation_events,                     -- Invitation events count
    silver.comment_events,                        -- Comment events count
    silver.crud_create_events,                    -- Create events count
    silver.crud_read_events,                      -- Read events count
    silver.crud_update_events,                    -- Update events count
    silver.crud_delete_events,                    -- Delete events count
    silver.invitation_invite_events,              -- Invite events count
    silver.comment_create_events,                 -- Comment creation events count
    silver.total_docs,                            -- Total documents
    silver.docs_with_crud_events,                 -- Docs with CRUD events
    silver.docs_with_invitation_events,           -- Docs with invitations
    silver.docs_with_comments_events,             -- Docs with comments
    silver.docs_with_crud_create_events,          -- Docs with create events
    silver.docs_with_crud_read_events,            -- Docs with read events
    silver.docs_with_crud_update_events,          -- Docs with update events
    silver.docs_with_crud_delete_events,          -- Docs with delete events
    silver.docs_with_invitation_invite_events,    -- Docs with invite events
    silver.docs_with_comment_create_events,       -- Docs with comment creation events

    -- Normalise entitlement type: FREE vs PAID
    CASE
        WHEN silver.user_properties.entitlement_type = 'FREE'
             AND silver.user_properties.entitlement_category IN ('CCE','CCT')
             AND silver.user_properties.offering_name IN (
                 'custom fonts','Free Membership','Free membership',
                 'Creative Cloud Shared Device Access – Higher-Ed',
                 'Adobe Express for K-12','Adobe Express for Education - K12 Edition',
                 'Complimentary Membership Teams','Adobe Express - K-12','AEMaaCS Trial Program'
             )
        THEN 'FREE'
        WHEN silver.user_properties.entitlement_category IN ('CCE','CCT') THEN 'PAID'
        ELSE silver.user_properties.entitlement_type
    END AS entitlement_type_updated,

    silver.user_properties.* EXCEPT(entitlement_type), -- Include all user properties except original entitlement_type

    -- Handle guest login separately
    CASE WHEN silver.user_properties.login_type = 'guest' THEN 'GUEST'
         ELSE silver.user_properties.entitlement_type
    END AS entitlement_type,

    silver.fiscal_week,                             -- Fiscal week identifier
    silver.period,                                  -- Period (MAU)
    
    -- Flag for latest or previous fiscal week
    CASE
        WHEN time.latest_fiscal_week = TO_DATE(silver.fiscal_wk_ending_date) THEN 1
        WHEN time.previous_fiscal_week = TO_DATE(silver.fiscal_wk_ending_date) THEN -1
        ELSE 0
    END AS max_time,

    TO_DATE(silver.fiscal_wk_ending_date) AS fiscal_week_ending_date -- Convert fiscal week end date to date
FROM acpm_warehouse.usage_metrics_user_details_silver silver

-- Join to map application to product and product group
LEFT JOIN (
    SELECT DISTINCT Application, Product, Product_Group
    FROM acpm_warehouse.ims_userclientid_to_app_mapping
) am ON am.Application = silver.application

-- Join to enrich with organisation details
LEFT JOIN (
    SELECT DISTINCT org_id, org_name, ech_parent_name, industry, ech_sub_industry
    FROM acpm_warehouse_test.org_mapping
) b2b ON b2b.org_id = silver.user_properties.org_id

-- Cross join to inject latest and previous fiscal week constants
CROSS JOIN (
    SELECT
        MAX(TO_DATE(g.fiscal_wk_ending_date)) AS latest_fiscal_week,
        MAX(TO_DATE(g.fiscal_wk_ending_date)) - 28 AS previous_fiscal_week
    FROM acpm_warehouse.usage_metrics_user_details_silver g
    WHERE period = 'MAU'
) time

-- Filters: only MAU period, exclude irrelevant asset types, and user-initiated events
WHERE silver.period = 'MAU'
  AND silver.construct.asset_type NOT IN ('directory', 'output')
  AND (
      silver.event_initiation_type = 'user'
      OR silver.event_initiation_type IS NULL
      OR silver.event_initiation_type = 'Unmapped'
  );