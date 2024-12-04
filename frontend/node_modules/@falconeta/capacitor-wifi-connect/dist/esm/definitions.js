export var ConnectState;
(function (ConnectState) {
    ConnectState[ConnectState["Ok"] = 0] = "Ok";
    ConnectState[ConnectState["Denied"] = -1] = "Denied";
    ConnectState[ConnectState["Ko"] = -2] = "Ko";
    ConnectState[ConnectState["UnknowSsid"] = -3] = "UnknowSsid";
    ConnectState[ConnectState["WifiDisabled"] = -4] = "WifiDisabled";
    ConnectState[ConnectState["AppLocalizationPermission"] = -5] = "AppLocalizationPermission";
    ConnectState[ConnectState["SystemLocalizationPermission"] = -6] = "SystemLocalizationPermission";
})(ConnectState || (ConnectState = {}));
//# sourceMappingURL=definitions.js.map